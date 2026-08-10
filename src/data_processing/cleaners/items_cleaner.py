"""
Enterprise Product Analytics Platform
Item Data Cleaner
"""

from loguru import logger


class ItemsCleaner:

    def remove_duplicates(self, dataframe):

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        logger.info(
            f"Removed {before - len(dataframe):,} duplicate rows"
        )

        return dataframe

    def clean(self, dataframe):

        logger.info("Starting Item Cleaning Pipeline")

        dataframe = dataframe.copy()

        dataframe.columns = [
            column.strip().lower()
            for column in dataframe.columns
        ]

        dataframe = self.remove_duplicates(dataframe)

        if "itemid" in dataframe.columns:
            dataframe = dataframe.dropna(
                subset=["itemid"]
            )

        logger.success("Item cleaning completed")

        return dataframe