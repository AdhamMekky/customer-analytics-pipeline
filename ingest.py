import sys
import pandas as pd
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <dataset_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    df.to_csv("data_raw.csv", index=False)
    print(f"[ingest] Loaded {len(df)} rows from '{input_path}' -> saved as data_raw.csv")

    subprocess.run([sys.executable, "preprocess.py", "data_raw.csv"], check=True)

if __name__ == "__main__":
    main()
