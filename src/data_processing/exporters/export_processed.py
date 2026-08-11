"""
Enterprise Product Analytics Platform
Processed Data Exporter

Exports cleaned and transformed datasets to the processed data directory.
"""

from pathlib import Path

import pandas as pd
from loguru import logger


class ProcessedDataExporter:

    def __init__(self, output_directory="data/processed"):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def export_csv(self, dataframe: pd.DataFrame, filename: str):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "dataframe must be a pandas DataFrame"
            )

        output_path = self.output_directory / filename

        if output_path.suffix.lower() != ".csv":
            output_path = output_path.with_suffix(".csv")

        dataframe.to_csv(
            output_path,
            index=False,
        )

        logger.success(
            f"Exported {len(dataframe):,} rows to {output_path}"
        )

        return output_path

    def export_parquet(self, dataframe: pd.DataFrame, filename: str):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "dataframe must be a pandas DataFrame"
            )

        output_path = self.output_directory / filename

        if output_path.suffix.lower() != ".parquet":
            output_path = output_path.with_suffix(".parquet")

        dataframe.to_parquet(
            output_path,
            index=False,
        )

        logger.success(
            f"Exported {len(dataframe):,} rows to {output_path}"
        )

        return output_path

    def export_dataset(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str,
        format="csv",
    ):

        if format.lower() == "csv":

            return self.export_csv(
                dataframe,
                f"{dataset_name}.csv",
            )

        if format.lower() == "parquet":

            return self.export_parquet(
                dataframe,
                f"{dataset_name}.parquet",
            )

        raise ValueError(
            "Unsupported format. Use 'csv' or 'parquet'."
        )

    def export_multiple(
        self,
        datasets: dict,
        format="csv",
    ):

        exported_files = {}

        for dataset_name, dataframe in datasets.items():

            exported_files[dataset_name] = (
                self.export_dataset(
                    dataframe,
                    dataset_name,
                    format,
                )
            )

        logger.success(
            f"Exported {len(exported_files)} datasets successfully"
        )

        return exported_files


if __name__ == "__main__":

    exporter = ProcessedDataExporter()

    sample_data = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "value": ["A", "B", "C"],
        }
    )

    output = exporter.export_dataset(
        sample_data,
        "sample_dataset",
        format="csv",
    )

    print(f"Export completed: {output}")