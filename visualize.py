import sys
import subprocess
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    numeric_df = df.select_dtypes(include=["number"])
    print(f"[visualize] Loaded {len(df)} rows from '{input_path}'")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Histogram of first numeric column
    first_col = numeric_df.columns[0]
    axes[0].hist(numeric_df[first_col], bins=15, color="steelblue", edgecolor="black")
    axes[0].set_title(f"Histogram of {first_col}")
    axes[0].set_xlabel(first_col)
    axes[0].set_ylabel("Frequency")

    # Plot 2: Correlation Heatmap
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=False, cmap="coolwarm", ax=axes[1], square=True)
    axes[1].set_title("Correlation Heatmap")

    # Plot 3: Scatter of PCA components (if available) or first two numeric cols
    if "PCA_1" in df.columns and "PCA_2" in df.columns:
        axes[2].scatter(df["PCA_1"], df["PCA_2"], alpha=0.6, c="teal", edgecolors="k", s=40)
        axes[2].set_title("PCA Component Scatter")
        axes[2].set_xlabel("PCA_1")
        axes[2].set_ylabel("PCA_2")
    else:
        c1, c2 = numeric_df.columns[0], numeric_df.columns[1]
        axes[2].scatter(numeric_df[c1], numeric_df[c2], alpha=0.6, c="teal", edgecolors="k", s=40)
        axes[2].set_title(f"{c1} vs {c2}")
        axes[2].set_xlabel(c1)
        axes[2].set_ylabel(c2)

    plt.tight_layout()
    plt.savefig("summary_plot.png", dpi=150)
    plt.close()
    print("  Saved summary_plot.png")

    subprocess.run([sys.executable, "cluster.py", input_path], check=True)

if __name__ == "__main__":
    main()
