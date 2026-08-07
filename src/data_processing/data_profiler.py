import pandas as pd
from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw" / "retailrocket"

datasets = {
    "Events": pd.read_csv(DATA_DIR / "events.csv"),
    "Item Properties Part 1": pd.read_csv(DATA_DIR / "item_properties_part1.csv"),
    "Item Properties Part 2": pd.read_csv(DATA_DIR / "item_properties_part2.csv"),
    "Category Tree": pd.read_csv(DATA_DIR / "category_tree.csv")
}

print("=" * 80)
print("ENTERPRISE PRODUCT ANALYTICS DATA PROFILER")
print("=" * 80)

for name, df in datasets.items():

    print("\n" + "=" * 80)
    print(name.upper())
    print("=" * 80)

    print(f"Rows                 : {df.shape[0]:,}")
    print(f"Columns              : {df.shape[1]}")
    print(f"Memory Usage (MB)    : {df.memory_usage(deep=True).sum()/1024**2:.2f}")

    print("\nData Types")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    print("\nUnique Values")
    print(df.nunique())

    print("\nSummary Statistics")
    print(df.describe(include="all").T)

print("\n")
print("=" * 80)
print("DATA PROFILING COMPLETED")
print("=" * 80)