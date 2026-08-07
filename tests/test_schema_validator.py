"""
Enterprise Product Analytics Platform

Test Schema Validator
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data_processing.loaders.csv_loader import CSVLoader
from src.data_processing.validators.schema_validator import SchemaValidator


def main():
    print("=" * 80)
    print("ENTERPRISE PRODUCT ANALYTICS PLATFORM")
    print("SCHEMA VALIDATION TEST")
    print("=" * 80)

    loader = CSVLoader()
    validator = SchemaValidator()

    datasets = loader.load_all()

    for dataset_name, dataframe in datasets.items():
        validator.validate(dataset_name, dataframe)

    print("=" * 80)
    print("✅ ALL DATASETS PASSED SCHEMA VALIDATION")
    print("=" * 80)


if __name__ == "__main__":
    main()