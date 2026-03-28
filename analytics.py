import sys
import subprocess
import pandas as pd

def main():
    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    print(f"[analytics] Loaded {len(df)} rows from '{input_path}'")

    # Insight 1: Summary statistics
    summary = df.describe().to_string()
    insight1 = (
        "=== Insight 1: Summary Statistics ===\n\n"
        f"The preprocessed dataset contains {df.shape[0]} samples and {df.shape[1]} features.\n\n"
        f"{summary}\n"
    )
    with open("insight1.txt", "w") as f:
        f.write(insight1)
    print("  Saved insight1.txt (summary statistics)")

    # Insight 2: Correlation analysis
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr()
    # Find top 5 strongest correlations (excluding self-correlation)
    pairs = []
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((cols[i], cols[j], corr.iloc[i, j]))
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    top_pairs = pairs[:5]

    insight2 = "=== Insight 2: Top Feature Correlations ===\n\n"
    for c1, c2, val in top_pairs:
        insight2 += f"  {c1} <-> {c2}: {val:.4f}\n"
    insight2 += (
        "\nHighly correlated features may indicate redundancy or strong linear "
        "relationships that clustering algorithms can exploit.\n"
    )
    with open("insight2.txt", "w") as f:
        f.write(insight2)
    print("  Saved insight2.txt (correlation analysis)")

    # Insight 3: Distribution of discretized bins
    insight3 = "=== Insight 3: Discretized Feature Distributions ===\n\n"
    bin_cols = [c for c in df.columns if c.endswith("_Bin")]
    if bin_cols:
        for col in bin_cols:
            counts = df[col].value_counts().sort_index()
            insight3 += f"{col}:\n"
            for val, cnt in counts.items():
                insight3 += f"  Bin {int(val)}: {cnt} samples ({cnt/len(df)*100:.1f}%)\n"
            insight3 += "\n"
        insight3 += "The bins were generated using quantile-based discretization.\n"
    else:
        insight3 += "No discretized bin columns found.\n"

    with open("insight3.txt", "w") as f:
        f.write(insight3)
    print("  Saved insight3.txt (bin distributions)")

    subprocess.run([sys.executable, "visualize.py", input_path], check=True)

if __name__ == "__main__":
    main()
