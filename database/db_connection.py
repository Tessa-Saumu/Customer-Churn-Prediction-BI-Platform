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

   # Enable foreign key enforcement. Although the current schema
    # contains only the customers table, enabling this ensures any
    # future foreign key relationships declared in schema.sql are
    # enforced by SQLite.
    connection.execute("PRAGMA foreign_keys = ON")

    logger.info("Connected to database at %s", DB_PATH.resolve())
    return connection