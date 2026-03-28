import sys
import subprocess
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, KBinsDiscretizer
from sklearn.decomposition import PCA

def main():
    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    print(f"[preprocess] Loaded {len(df)} rows from '{input_path}'")

    # ── Data Cleaning ──
    # 1. Remove duplicate rows
    before = len(df)
    df.drop_duplicates(inplace=True)
    print(f"  Removed {before - len(df)} duplicate rows")

    # 2. Handle missing values: median for numeric, mode for categorical
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    # 3. Drop CustomerID as it's not a useful feature
    if "CustomerID" in df.columns:
        df.drop(columns=["CustomerID"], inplace=True)

    # ── Feature Transformation ──
    # 1. Encode categorical columns with LabelEncoder
    label_encoders = {}
    for col in df.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"  Encoded '{col}' -> {list(le.classes_)}")

    # 2. Scale numeric columns with StandardScaler
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # 3. Create interaction feature: Income * Spending
    if "Annual_Income" in df.columns and "Spending_Score" in df.columns:
        df["Income_Spending_Interaction"] = df["Annual_Income"] * df["Spending_Score"]

    # ── Dimensionality Reduction ──
    # Apply PCA to reduce to 3 principal components (keep original cols too)
    pca_cols = [c for c in numeric_cols if c in df.columns]
    if len(pca_cols) >= 3:
        pca = PCA(n_components=3)
        pca_result = pca.fit_transform(df[pca_cols])
        df["PCA_1"] = pca_result[:, 0]
        df["PCA_2"] = pca_result[:, 1]
        df["PCA_3"] = pca_result[:, 2]
        explained = sum(pca.explained_variance_ratio_) * 100
        print(f"  PCA: 3 components explain {explained:.1f}% of variance")

    # ── Discretization ──
    # 1. Bin Age into 3 categories (Young / Adult / Senior)
    if "Age" in df.columns:
        kbd = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile")
        df["Age_Bin"] = kbd.fit_transform(df[["Age"]]).astype(int)
        print("  Discretized 'Age' into 3 bins")

    # 2. Bin Annual_Income into 3 tiers (Low / Medium / High)
    if "Annual_Income" in df.columns:
        kbd2 = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile")
        df["Income_Bin"] = kbd2.fit_transform(df[["Annual_Income"]]).astype(int)
        print("  Discretized 'Annual_Income' into 3 bins")

    # 3. Bin Spending_Score into 3 levels
    if "Spending_Score" in df.columns:
        kbd3 = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile")
        df["Spending_Bin"] = kbd3.fit_transform(df[["Spending_Score"]]).astype(int)
        print("  Discretized 'Spending_Score' into 3 bins")

    df.to_csv("data_preprocessed.csv", index=False)
    print(f"[preprocess] Saved data_preprocessed.csv ({df.shape[0]} rows, {df.shape[1]} cols)")

    subprocess.run([sys.executable, "analytics.py", "data_preprocessed.csv"], check=True)

if __name__ == "__main__":
    main()
