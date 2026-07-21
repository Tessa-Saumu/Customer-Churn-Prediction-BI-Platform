"""
Issue #8 -- ETL & Database -- etl/clean_data.py

total_charges handling and the customer_id rename below are Mercy's
work, unchanged. This pass removes a duplicated conversion call,
fixes indentation, and drops the "count" column to match schema.sql.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names to lowercase_with_underscores.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    # Rename customerid to customer_id so the cleaned dataset,
    # database schema, and repository layer all use the same
    # primary key naming convention.
    df = df.rename(columns={"customerid": "customer_id"})

    # "count" is a constant-1 utility column from the source Cognos
    # export with no business meaning -- dropped to match schema.sql.
    # Row counts belong in application code (len(df)), not stored
    # per-row in the database.
    df = df.drop(columns=["count"])
    logger.info("Column names standardized.")

    # Strip leading/trailing whitespace from all string columns.
    object_columns = df.select_dtypes(include="object").columns
    for col in object_columns:
        df[col] = df[col].str.strip()
    logger.info("Removed extra whitespace from string columns.")

    # Drop exact duplicate rows.
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        df = df.drop_duplicates()
        logger.info("Removed %d duplicate rows.", duplicate_count)
    else:
        logger.info("No duplicate rows found.")

    # total_charges needs to become numeric -- some rows have
    # non-numeric values here for a specific category of customer.
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    logger.info("Converted total_charges to numeric.")

    # Log how many values became missing after conversion.
    null_count = df["total_charges"].isna().sum()
    logger.info("Null values in total_charges after conversion: %d", null_count)

    # Inspect the affected rows to understand why total_charges is missing.
    if null_count > 0:
        logger.info(
            "Rows with missing total_charges:\n%s",
            df.loc[
                df["total_charges"].isna(),
                ["customer_id", "tenure_months", "monthly_charges", "contract", "churn_label"],
            ],
        )

    # Customers with zero months of tenure have not completed their first
    # billing cycle. For these customers, a missing total_charges value
    # represents zero accumulated charges rather than missing data.
    df["total_charges"] = df["total_charges"].fillna(0)

    # Churn reason is only applicable to customers who churned.
    df["churn_reason"] = df["churn_reason"].fillna("Not Applicable")

    logger.info("Rows after cleaning: %d", len(df))
    logger.info("Dataset cleaned successfully.")

    return df


if __name__ == "__main__":
    # Optional: lets you run this file on its own for a quick check
    # while you're working, without needing load_to_db.py finished yet.
    import logging as _logging
    import sys
    from pathlib import Path as _Path

    _repo_root = _Path(__file__).resolve().parent.parent
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))

    from etl.inspect_raw_data import DATASET_PATH, load_data

    _logging.basicConfig(level=_logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cleaned = clean_data(load_data(DATASET_PATH))
    logger.info("Standalone clean_data run complete. Final shape: %s", cleaned.shape)