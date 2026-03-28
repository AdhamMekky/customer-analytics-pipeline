import sys
import pandas as pd
from sklearn.cluster import KMeans

def main():
    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    numeric_df = df.select_dtypes(include=["number"])
    print(f"[cluster] Loaded {len(df)} rows from '{input_path}'")

    # Use PCA components if available, otherwise use all numeric features
    if all(c in df.columns for c in ["PCA_1", "PCA_2", "PCA_3"]):
        features = df[["PCA_1", "PCA_2", "PCA_3"]]
    else:
        features = numeric_df

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features)

    output = "=== K-Means Clustering Results ===\n\n"
    output += f"Number of clusters: 4\n"
    output += f"Features used: {list(features.columns)}\n\n"
    output += "Samples per cluster:\n"
    for cluster_id in sorted(set(labels)):
        count = (labels == cluster_id).sum()
        output += f"  Cluster {cluster_id}: {count} samples\n"

    with open("clusters.txt", "w") as f:
        f.write(output)
    print("  Saved clusters.txt")
    print("[pipeline] All steps completed successfully.")

if __name__ == "__main__":
    main()
