"""
Issue #8 -- ETL & Database -- etl/clean_data.py

Owns this part of the spec (Project_Specification.md section 2.1):
"etl/clean_data.py handles missing values with a documented strategy
(code comment explaining the choice, not just the code)."

Most of this is already correct and carried over from your original
inspect_raw_data.py draft -- column standardization, whitespace
stripping, and dedup all worked, so they're kept as-is. ONE thing is
intentionally left for you below. Everything else is here so today's
time goes toward that one decision instead of rebuilding what already
worked.

Downstream dependency: Latifah's model training (Issue #11) and
etl/load_to_db.py both consume whatever this function returns. If the
output's shape (column names, dtypes) changes, flag it -- don't let it
change silently.
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

    # --- TODO (yours to finish) -------------------------------------
    # total_charges needs to become numeric, but this dataset is known
    # to have some non-numeric values in that column for a specific
    # category of customer. pd.to_numeric(..., errors="coerce") below
    # will silently turn anything non-numeric into NaN -- converting it
    # is necessary, but converting it is NOT the same as handling it. A
    # coerced NaN is still a missing value once the conversion is done,
    # and the spec requires missing values to be handled with a
    # *documented* strategy, not just produced.
    #
    # Your job, in order:
    #   1. Log the null count on total_charges right after the
    #      conversion below -- is it actually zero, or not?
    #   2. If it's not zero, look at which rows those are. Is there a
    #      pattern? (Hint: check what else is true about those specific
    #      customers.)
    #   3. Decide what should happen to them -- there's a real,
    #      defensible business reason certain customers would have $0
    #      or no charges recorded yet, which is different from missing
    #      data that should be imputed or dropped.
    #   4. Write a comment here explaining the decision you made, same
    #      as churn_reason is documented below.
    # ------------------------------------------------------------------
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    logger.info("Converted total_charges to numeric.")
    # <-- your fillna/decision for total_charges goes here, with a comment
    #     explaining why, right above the line that implements it.

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

    # Needed because the README runs files like this directly
    # (`python3 etl/clean_data.py`), which only puts this file's own
    # directory on sys.path -- without this, the sibling-package import
    # just below would fail to resolve.
    _repo_root = _Path(__file__).resolve().parent.parent
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))

    from etl.inspect_raw_data import DATASET_PATH, load_data

    _logging.basicConfig(level=_logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cleaned = clean_data(load_data(DATASET_PATH))
    logger.info("Standalone clean_data run complete. Final shape: %s", cleaned.shape)