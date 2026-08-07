import pandas as pd
from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw" / "retailrocket"

EVENTS_FILE = DATA_DIR / "events.csv"
ITEM_PROPERTIES_1 = DATA_DIR / "item_properties_part1.csv"
ITEM_PROPERTIES_2 = DATA_DIR / "item_properties_part2.csv"
CATEGORY_TREE = DATA_DIR / "category_tree.csv"

# ==========================================================
# CHECK FILES
# ==========================================================

files = {
    "Events": EVENTS_FILE,
    "Item Properties Part 1": ITEM_PROPERTIES_1,
    "Item Properties Part 2": ITEM_PROPERTIES_2,
    "Category Tree": CATEGORY_TREE
}

print("=" * 70)
print("ENTERPRISE PRODUCT ANALYTICS PLATFORM")
print("RetailRocket Data Loader")
print("=" * 70)

for name, path in files.items():

    if path.exists():
        print(f"✅ {name:<25} Found")
    else:
        print(f"❌ {name:<25} Missing")

print("=" * 70)

# ==========================================================
# LOAD DATASETS
# ==========================================================

events = pd.read_csv(EVENTS_FILE)

item_properties_1 = pd.read_csv(ITEM_PROPERTIES_1)

item_properties_2 = pd.read_csv(ITEM_PROPERTIES_2)

category_tree = pd.read_csv(CATEGORY_TREE)

# ==========================================================
# DATASET INFORMATION
# ==========================================================

datasets = {
    "Events": events,
    "Item Properties Part 1": item_properties_1,
    "Item Properties Part 2": item_properties_2,
    "Category Tree": category_tree
}

for name, df in datasets.items():

    print("\n" + "=" * 70)
    print(name.upper())
    print("=" * 70)

    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns")

    print(df.columns.tolist())

    print("\nData Types")

    print(df.dtypes)

    print("\nFirst Five Rows")

    print(df.head())

print("\n")
print("=" * 70)
print("ALL DATASETS LOADED SUCCESSFULLY")
print("=" * 70)