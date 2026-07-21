"""
Issue #8 -- ETL & Database -- etl/inspect_raw_data.py
"""

import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATASET_PATH = "data/raw/telco_churn_raw.csv"


def load_data(path: str) -> pd.DataFrame:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path.resolve()}"
        )

    # dtype={"Zip Code": str} -- without this, pandas infers Zip Code
    # as int64 at read time and silently drops any leading zero
    # (00101 becomes 101) before any downstream code ever sees it.
    # Fixing the column's type in schema.sql alone doesn't help if the
    # zero is already gone by this point.
    df = pd.read_csv(file_path, dtype={"Zip Code": str})
    logger.info("Dataset loaded successfully. Rows loaded: %d", len(df))

    return df


def inspect_data(df: pd.DataFrame) -> None:
    logger.info("Rows: %d", df.shape[0])
    logger.info("Columns: %d", df.shape[1])

    logger.info("Column Names: %s", df.columns.tolist())
    logger.info("Data Types:\n%s", df.dtypes)
    logger.info("Missing Values:\n%s", df.isnull().sum())
    logger.info("Duplicate Rows: %d", df.duplicated().sum())
    logger.info("Unique Values Per Column:\n%s", df.nunique())
    logger.info("Summary Statistics:\n%s", df.describe(include="all"))


if __name__ == "__main__":
    raw_df = load_data(DATASET_PATH)
    inspect_data(raw_df)