"""
Issue #8 -- ETL & Database -- database/init_db.py

Reads and executes sql/schema.sql against the database. Must be
idempotent -- running this twice in a row must not raise an error,
which is why every CREATE TABLE in schema.sql needs
IF NOT EXISTS (that's on you in schema.sql, not this file).
"""

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
# ^ needed because the README runs this as `python3 database/init_db.py`
# (a direct script call, not `python -m`), which only puts this file's
# own directory on sys.path. Without this, the import below would fail
# to resolve `database` as a package. Same fix appears in
# etl/load_to_db.py and app/repository/customer_repository.py for the
# same reason.

from database.db_connection import get_connection

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path("sql/schema.sql")


def init_db() -> None:
    schema_sql = SCHEMA_PATH.read_text()

    connection = get_connection()
    try:
        connection.executescript(schema_sql)
        connection.commit()
        logger.info("Database initialized from %s", SCHEMA_PATH)
    finally:
        connection.close()

    # TODO: once schema.sql has your real columns in it, run this file
    # twice in a row from the command line and confirm the second run
    # doesn't raise -- that's the acceptance criterion, and it's a
    # two-minute check once schema.sql is filled in.


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    init_db()