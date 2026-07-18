"""
Issue #8 -- ETL & Database -- database/db_connection.py

This pattern doesn't depend on your specific data, so it's given in
full except for one small decision flagged below.
"""

import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path("database/churn.db")


def get_connection() -> sqlite3.Connection:
    """
    Returns a connection to database/churn.db, creating the file (and
    its parent directory) if either doesn't exist yet.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)

    # TODO: decide whether to turn on foreign key enforcement --
    # PRAGMA foreign_keys = ON. SQLite ignores foreign key constraints
    # by default even when they're declared in schema.sql. If you ended
    # up adding a related table with a foreign key back to customers in
    # schema.sql, you'll want this on. If customers is your only table,
    # this is a no-op either way, so it's safe to enable regardless --
    # just uncomment the line below once you've made the call.
    # connection.execute("PRAGMA foreign_keys = ON")

    logger.info("Connected to database at %s", DB_PATH.resolve())
    return connection