import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database/churn.db")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def test_view_churn_by_contract_exists():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='view'
        AND name='view_churn_by_contract'
    """)

    assert cursor.fetchone() is not None

    conn.close()


def test_view_churn_by_tenure_bucket_exists():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='view'
        AND name='view_churn_by_tenure_bucket'
    """)

    assert cursor.fetchone() is not None

    conn.close()


def test_contract_view_returns_data():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM view_churn_by_contract
    """)

    assert cursor.fetchone()[0] > 0

    conn.close()


def test_tenure_view_returns_data():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM view_churn_by_tenure_bucket
    """)

    assert cursor.fetchone()[0] > 0

    conn.close()


def test_contract_view_contains_expected_columns():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM view_churn_by_contract
        LIMIT 1
    """)

    columns = [column[0] for column in cursor.description]

    expected = [
        "Contract",
        "total_customers",
        "churned_customers",
        "churn_rate_percentage",
    ]

    assert columns == expected

    conn.close()


def test_tenure_view_contains_expected_columns():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM view_churn_by_tenure_bucket
        LIMIT 1
    """)

    columns = [column[0] for column in cursor.description]

    expected = [
        "tenure_bucket",
        "total_customers",
        "churned_customers",
        "churn_rate_percentage",
    ]

    assert columns == expected

    conn.close()