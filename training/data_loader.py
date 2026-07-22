import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd

from database.db_connection import get_connection


logger = logging.getLogger(__name__)


def load_training_data() -> pd.DataFrame:
    """
    Load customer data from the SQLite database.
    Returns a pd.DataFrame, a Customer records used for model training.
    """
    connection = get_connection()

    try:
        query = "SELECT * FROM customers"
        df = pd.read_sql_query(query, connection)

        logger.info("Loaded %d customer records.", len(df))

        return df

    finally:
        connection.close()