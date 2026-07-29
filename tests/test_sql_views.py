"""
Issue #19 -- Full Regression Pass -- tests/test_sql_views.py

Owner: Salome, edited by Theresia, added during the Issue #19 full regression pass.
This file predates Issue #19.
(it already existed and passed once the full pipeline had been run
locally), but had no skip-guard, so it hard-FAILED rather than
SKIPPED on a fresh clone -- the only one of the four test files in
tests/ that behaved this way. See docs/qa_findings.md's Issue #19
section for the full writeup of this finding.

Prerequisites
-------------
These tests assume sql/views.sql has already been applied to
database/churn.db via:

    python database/init_db.py
    python etl/load_to_db.py
    python database/init_views.py

If database/churn.db does not exist, or either view is missing (e.g.
init_views.py has not been run yet), these tests SKIP with a clear
reason -- matching the pattern already used by
tests/test_etl.py::requires_populated_db and
tests/test_models.py::requires_populated_db/requires_model_artifact --
rather than failing with a confusing sqlite3.OperationalError.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database.db_connection import get_connection

DB_PATH = REPO_ROOT / "database" / "churn.db"

REQUIRED_VIEWS = ("view_churn_by_contract", "view_churn_by_tenure_bucket")


def _views_exist() -> bool:
    """
    True if database/churn.db exists AND both required views have
    been created in it. Used to skip gracefully on a fresh clone, or
    after the ETL pipeline has run but before database/init_views.py
    has -- both are legitimate pre-pipeline states, not bugs.
    """
    if not DB_PATH.exists():
        return False
    try:
        conn = get_connection()
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='view'"
            )
            existing = {row[0] for row in cursor.fetchall()}
            return all(view in existing for view in REQUIRED_VIEWS)
        finally:
            conn.close()
    except sqlite3.OperationalError:
        return False


requires_views = pytest.mark.skipif(
    not _views_exist(),
    reason=(
        "database/churn.db is missing, or view_churn_by_contract / "
        "view_churn_by_tenure_bucket have not been created yet. Run "
        "the full pipeline first (see README 'Run the ETL pipeline'): "
        "python database/init_db.py && python etl/load_to_db.py && "
        "python database/init_views.py"
    ),
)


@pytest.mark.integration
@requires_views
class TestViewsExist:
    """Verify both required analytical views exist in the schema."""

    def test_view_churn_by_contract_exists(self) -> None:
        """Verify the contract churn view exists."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='view'
            AND name='view_churn_by_contract'
            """
        )

        assert cursor.fetchone() is not None

        conn.close()

    def test_view_churn_by_tenure_bucket_exists(self) -> None:
        """Verify the tenure bucket churn view exists."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='view'
            AND name='view_churn_by_tenure_bucket'
            """
        )

        assert cursor.fetchone() is not None

        conn.close()


@pytest.mark.integration
@requires_views
class TestViewsReturnData:
    """Verify both views return rows once the pipeline has populated the database."""

    def test_contract_view_returns_data(self) -> None:
        """Verify the contract churn view returns rows."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM view_churn_by_contract
            """
        )

        assert cursor.fetchone()[0] > 0

        conn.close()

    def test_tenure_view_returns_data(self) -> None:
        """Verify the tenure bucket churn view returns rows."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM view_churn_by_tenure_bucket
            """
        )

        assert cursor.fetchone()[0] > 0

        conn.close()


@pytest.mark.integration
@requires_views
class TestViewSchemas:
    """Verify both views expose the exact columns the dashboard depends on."""

    def test_contract_view_contains_expected_columns(self) -> None:
        """Verify the contract churn view exposes the expected columns."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT *
            FROM view_churn_by_contract
            LIMIT 1
            """
        )

        columns = [column[0] for column in cursor.description]

        expected = [
            "contract",
            "total_customers",
            "churned_customers",
            "churn_rate_percentage",
        ]

        assert columns == expected

        conn.close()

    def test_tenure_view_contains_expected_columns(self) -> None:
        """Verify the tenure bucket churn view exposes the expected columns."""
        conn = get_connection()

        cursor = conn.execute(
            """
            SELECT *
            FROM view_churn_by_tenure_bucket
            LIMIT 1
            """
        )

        columns = [column[0] for column in cursor.description]

        expected = [
            "tenure_bucket",
            "total_customers",
            "churned_customers",
            "churn_rate_percentage",
        ]

        assert columns == expected

        conn.close()


@pytest.mark.integration
class TestViewsIdempotency:
    """
    Confirms database/init_views.py itself is safe to run repeatedly --
    a gap identified during the Issue #19 walkthrough:
    database/init_db.py has dedicated idempotency coverage in
    tests/test_etl.py::TestDatabaseIdempotency, but init_views.py had
    no equivalent test anywhere despite following the same
    drop-and-recreate pattern (see its own docstring).
    """

    def test_init_views_can_run_twice_without_error(self) -> None:
        if not DB_PATH.exists():
            pytest.skip(
                "database/churn.db is missing. Run python "
                "database/init_db.py first."
            )

        from database.init_views import init_views

        # Running twice back-to-back must not raise, and must leave
        # both views queryable afterward -- mirrors
        # TestDatabaseIdempotency's pattern for init_db() in
        # tests/test_etl.py.
        init_views()
        init_views()

        conn = get_connection()
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='view'"
            )
            existing = {row[0] for row in cursor.fetchall()}
        finally:
            conn.close()

        for view in REQUIRED_VIEWS:
            assert view in existing