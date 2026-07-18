"""
Issue #8 -- ETL & Database -- etl/inspect_raw_data.py

STATUS: repaired by Theresia ahead of the rewrite pass. The inspection
logic here was already solid, so only housekeeping changed:

  1. DATASET_PATH now matches the spec exactly
     (data/raw/telco_churn_raw.csv -- it previously pointed at
     data/raw/telco_customer_churn.csv, which doesn't match what the
     issue and spec both require).
  2. print() -> logging, per the project's cross-cutting standard and
     the issue's explicit acceptance criterion ("No print() statements
     exist in etl/ or database/"). Use this file as your reference for
     how that swap should look in clean_data.py, init_db.py, and
     load_to_db.py -- same pattern each time.
  3. clean_data() and validate_data() have moved out to
     etl/clean_data.py, which is where they belong per the spec (this
     file's contract is inspection only: column names, dtypes, null
     counts, row/column counts -- nothing else).

Go to etl/clean_data.py next -- there's one real decision left there
for you to make.
"""

import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATASET_PATH = "data/raw/telco_churn_raw.csv"


from pathlib import Path

def load_data(path: str) -> pd.DataFrame:

    file_path = Path(path)

    print("Current working directory:", Path.cwd())
    print("Looking for dataset at:", file_path.resolve())

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path.resolve()}"
        )

    return pd.read_csv(file_path)


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