"""
Initializes SQL views for analytics.

Reads and executes sql/views.sql against the SQLite database.

The initialization is idempotent by dropping existing views before
recreating them from sql/views.sql.
"""

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database.db_connection import get_connection

logger = logging.getLogger(__name__)

VIEWS_PATH = Path("sql/views.sql")


def init_views() -> None:
    """Create analytical SQL views."""

    views_sql = VIEWS_PATH.read_text(encoding="utf-8")

    connection = get_connection()

    try:
        # Drop existing views so the latest definitions are always applied.
        connection.executescript("""
        DROP VIEW IF EXISTS view_churn_by_contract;
        DROP VIEW IF EXISTS view_churn_by_tenure_bucket;
        """)

        # Create the views from the SQL script.
        connection.executescript(views_sql)
        connection.commit()

        logger.info("Views initialized from %s", VIEWS_PATH)

    finally:
        connection.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    init_views()