"""
Enterprise Product Analytics Platform
Category Data Cleaner
"""

from loguru import logger


class CategoryCleaner:

    def remove_duplicates(self, dataframe):

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        logger.info(
            f"Removed {before - len(dataframe):,} duplicate rows"
        )

        return dataframe

    def clean(self, dataframe):

        logger.info("Starting Category Cleaning Pipeline")

        dataframe = dataframe.copy()

        dataframe.columns = [
            column.strip().lower()
            for column in dataframe.columns
        ]

        dataframe = self.remove_duplicates(dataframe)

        if "categoryid" in dataframe.columns:
            dataframe = dataframe.dropna(
                subset=["categoryid"]
            )

        logger.success("Category cleaning completed")

        return dataframe