"""
Enterprise Product Analytics Platform
Data Processing Pipeline

Orchestrates loading, cleaning, validation, feature engineering,
and warehouse loading.
"""

from loguru import logger

from src.data_processing.loaders.csv_loader import CSVLoader
from src.data_processing.cleaners.events_cleaner import EventsCleaner
from src.data_processing.cleaners.items_cleaner import ItemsCleaner
from src.data_processing.cleaners.category_cleaner import CategoryCleaner
from src.data_processing.validators.schema_validator import SchemaValidator
from src.data_processing.validators.data_validator import DataValidator


class DataProcessingPipeline:

    def __init__(self):

        self.loader = CSVLoader()

        self.events_cleaner = EventsCleaner()
        self.items_cleaner = ItemsCleaner()
        self.category_cleaner = CategoryCleaner()

        self.schema_validator = SchemaValidator()
        self.data_validator = DataValidator()

    def run_events_pipeline(self):

        logger.info("=" * 80)
        logger.info("EVENTS DATA PIPELINE")
        logger.info("=" * 80)

        events = self.loader.load_csv("events.csv")

        self.schema_validator.validate(
            "events",
            events,
        )

        events = self.events_cleaner.clean(events)

        self.data_validator.validate(events)

        logger.success(
            f"Events pipeline completed: {len(events):,} rows"
        )

        return events

    def run_items_pipeline(self):

        logger.info("=" * 80)
        logger.info("ITEMS DATA PIPELINE")
        logger.info("=" * 80)

        item_part1 = self.loader.load_csv(
            "item_properties_part1.csv"
        )

        item_part2 = self.loader.load_csv(
            "item_properties_part2.csv"
        )

        items = item_part1

        if item_part2 is not None:
            import pandas as pd

            items = pd.concat(
                [item_part1, item_part2],
                ignore_index=True,
            )

        items = self.items_cleaner.clean(items)

        self.data_validator.validate(items)

        logger.success(
            f"Items pipeline completed: {len(items):,} rows"
        )

        return items

    def run_category_pipeline(self):

        logger.info("=" * 80)
        logger.info("CATEGORY DATA PIPELINE")
        logger.info("=" * 80)

        categories = self.loader.load_csv(
            "category_tree.csv"
        )

        categories = self.category_cleaner.clean(
            categories
        )

        self.data_validator.validate(categories)

        logger.success(
            f"Category pipeline completed: {len(categories):,} rows"
        )

        return categories

    def run(self):

        logger.info("=" * 80)
        logger.info("ENTERPRISE DATA PROCESSING PIPELINE")
        logger.info("=" * 80)

        results = {}

        results["events"] = self.run_events_pipeline()
        results["items"] = self.run_items_pipeline()
        results["categories"] = self.run_category_pipeline()

        logger.success("=" * 80)
        logger.success("ALL DATA PROCESSING PIPELINES COMPLETED")
        logger.success("=" * 80)

        return results


def main():

    pipeline = DataProcessingPipeline()

    results = pipeline.run()

    print("\nPIPELINE SUMMARY")
    print("=" * 80)

    for name, dataframe in results.items():
        print(
            f"{name:<15} : "
            f"{len(dataframe):,} rows × "
            f"{len(dataframe.columns)} columns"
        )


if __name__ == "__main__":
    main()