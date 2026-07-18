"""
Issue #8 -- ETL & Database -- etl/load_to_db.py

Loads the cleaned data into the customers table in SQLite. This is the
step that makes the "SQLite database" half of the issue real -- right
now the only "load" step that exists writes a CSV, not database rows.

TODO (yours to finish): the insert logic below is intentionally left
for you, since it depends on the exact column names you land on in
schema.sql -- there's no way to write this correctly without knowing
your final schema first. Do sql/schema.sql and database/init_db.py
before this file.
"""

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database.db_connection import get_connection
from etl.clean_data import clean_data
from etl.inspect_raw_data import DATASET_PATH, load_data

logger = logging.getLogger(__name__)


def load_to_db() -> None:
    raw_df = load_data(DATASET_PATH)
    clean_df = clean_data(raw_df)
    logger.info("Rows ready to insert: %d", len(clean_df))

    connection = get_connection()
    try:
        # TODO: insert clean_df into the customers table. The simplest
        # correct approach is:
        #
        #   clean_df.to_sql("customers", connection,
        #                    if_exists="append", index=False)
        #
        # A few things to actually check before you run this, not just
        # copy it:
        #   - clean_df's column names must match schema.sql's column
        #     names exactly -- to_sql will not warn you if they don't
        #     line up the way you think they do.
        #   - use if_exists="append", not "replace" -- "replace" would
        #     drop the table init_db.py just created from schema.sql.
        #   - if you need this to be safely re-runnable without
        #     duplicating rows, delete existing rows first
        #     (connection.execute("DELETE FROM customers")) before the
        #     insert, or dedupe on customer_id afterward -- your call,
        #     just be deliberate about it.
        #
        # Log the row count actually inserted once this runs -- that's
        # one of the three required log points for this issue ("rows
        # inserted").
        pass
    finally:
        connection.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_to_db()