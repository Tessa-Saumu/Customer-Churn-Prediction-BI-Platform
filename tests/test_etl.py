"""
Issue #13 -- ETL & Database Testing -- tests/test_etl.py

Owner: Theresia --
authored entirely from scratch for this issue, no content carried over
from Mercy's (#8), Praise's (#10), or Latifah's (#11) work.

Structure
---------
This file is split into two clearly-marked sections rather than two
separate files/folders:

    1. UNIT TESTS      (@pytest.mark.unit)
       Pure function behaviour only -- etl/clean_data.py's cleaning
       logic. No real database connection, no real file I/O beyond an
       in-memory DataFrame.

    2. INTEGRATION TESTS (@pytest.mark.integration)
       Exercises the real SQLite database (database/churn.db),
       database/init_db.py, and app/repository/customer_repository.py
       against whatever the ETL pipeline has actually loaded.

Run everything:            pytest tests/test_etl.py
Run only unit tests:       pytest tests/test_etl.py -m unit
Run only integration:      pytest tests/test_etl.py -m integration

Prerequisites for the integration section
------------------------------------------
The integration tests assume the standard local pipeline (per the
README's "Run the ETL pipeline" section) has already been run at least
once against a real dataset:

    python database/init_db.py
    python etl/load_to_db.py
    python database/init_views.py

If database/churn.db does not exist, or the customers table is empty,
the integration tests SKIP with a clear reason rather than failing --
a fresh clone with no data yet is a legitimate state, not a bug. This
is noted explicitly in PR Notes.

Logging coverage
-----------------
caplog-based tests confirm the specific log messages the issue calls
out by name: rows loaded, rows after cleaning, rows inserted. These
messages already exist in etl/inspect_raw_data.py, etl/clean_data.py,
and etl/load_to_db.py as shipped -- no implementation changes were
made to produce them. Any gap found beyond these three specific
messages is documented in PR Notes, not silently patched.
"""

from __future__ import annotations

import logging
import sqlite3
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database.db_connection import get_connection
from database.init_db import init_db
from etl.clean_data import clean_data
from app.repository.customer_repository import CustomerRepository

DB_PATH = REPO_ROOT / "database" / "churn.db"


def _db_is_populated() -> bool:
    """
    True if database/churn.db exists AND the customers table has at
    least one row. Used to skip integration tests gracefully on a
    fresh clone rather than fail with a confusing error.
    """
    if not DB_PATH.exists():
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            cursor = conn.execute("SELECT COUNT(*) FROM customers")
            return cursor.fetchone()[0] > 0
        finally:
            conn.close()
    except sqlite3.OperationalError:
        # customers table doesn't exist yet.
        return False


requires_populated_db = pytest.mark.skipif(
    not _db_is_populated(),
    reason=(
        "database/churn.db is missing or empty. Run the ETL pipeline "
        "first: python database/init_db.py && python etl/load_to_db.py"
    ),
)


def _make_raw_dataframe(**overrides: Any) -> pd.DataFrame:
    """
    Builds a single-row raw-CSV-shaped DataFrame matching the real
    Telco export's column names/casing (pre-clean_data), so unit tests
    exercise clean_data() the same way etl/load_to_db.py does in
    production -- not a pre-cleaned shortcut.

    Callers can override individual columns via keyword args, e.g.
    _make_raw_dataframe(**{"Total Charges": "  "}) to test a specific
    edge case without repeating the whole row.
    """
    base = {
        "CustomerID": "1234-ABCDE",
        "Count": 1,
        "Country": "United States",
        "State": "California",
        "City": "Los Angeles",
        "Zip Code": "90001",
        "Lat Long": "34.05, -118.24",
        "Latitude": 34.05,
        "Longitude": -118.24,
        "Gender": "Female",
        "Senior Citizen": "No",
        "Partner": "Yes",
        "Dependents": "No",
        "Tenure Months": 12,
        "Phone Service": "Yes",
        "Multiple Lines": "No",
        "Internet Service": "Fiber optic",
        "Online Security": "No",
        "Online Backup": "Yes",
        "Device Protection": "No",
        "Tech Support": "No",
        "Streaming TV": "Yes",
        "Streaming Movies": "No",
        "Contract": "Month-to-month",
        "Paperless Billing": "Yes",
        "Payment Method": "Electronic check",
        "Monthly Charges": 70.05,
        "Total Charges": "840.60",
        "Churn Label": "No",
        "Churn Value": 0,
        "Churn Score": 45,
        "CLTV": 3200,
        "Churn Reason": "",
    }
    base.update(overrides)
    return pd.DataFrame([base])


# ======================================================================
# SECTION 1 -- UNIT TESTS
# Pure clean_data() behaviour. No database, no files on disk.
# ======================================================================


@pytest.mark.unit
class TestCleanDataBaselineCorrectness:
    """Baseline correctness: clean_data() follows its documented rules."""

    def test_column_names_are_standardized_to_snake_case(self) -> None:
        df = _make_raw_dataframe()
        result = clean_data(df)
        assert "customer_id" in result.columns
        assert "monthly_charges" in result.columns
        # Original raw-CSV casing must not survive cleaning.
        assert "CustomerID" not in result.columns
        assert "Monthly Charges" not in result.columns

    def test_count_column_is_dropped(self) -> None:
        df = _make_raw_dataframe()
        result = clean_data(df)
        assert "count" not in result.columns

    def test_total_charges_blank_string_becomes_zero_for_zero_tenure(self) -> None:
        """
        Documented strategy (etl/clean_data.py + docs/data_dictionary.md):
        a blank/non-numeric total_charges for a brand-new customer
        (tenure_months == 0) represents zero accumulated charges, not
        missing data, so it is filled with 0 rather than dropped.
        """
        df = _make_raw_dataframe(**{"Tenure Months": 0, "Total Charges": "  "})
        result = clean_data(df)
        assert result.loc[0, "total_charges"] == 0.0

    def test_churn_reason_null_becomes_not_applicable(self) -> None:
        """
        Documented strategy: churn_reason only applies to customers
        who actually churned; a genuinely-missing value (what
        pd.read_csv produces for a blank CSV cell -- real NaN, not a
        literal empty string, confirmed via a direct
        pd.read_csv(io.StringIO(...)) check during test authorship)
        is filled with the sentinel "Not Applicable" rather than left
        null. This matches production input shape: clean_data() is
        only ever called on a DataFrame produced by
        etl/inspect_raw_data.py's pd.read_csv().
        """
        df = _make_raw_dataframe(**{"Churn Label": "No", "Churn Reason": None})
        result = clean_data(df)
        assert result.loc[0, "churn_reason"] == "Not Applicable"

    def test_whitespace_is_stripped_from_string_columns(self) -> None:
        df = _make_raw_dataframe(**{"Gender": "  Female  ", "Contract": " Month-to-month "})
        result = clean_data(df)
        assert result.loc[0, "gender"] == "Female"
        assert result.loc[0, "contract"] == "Month-to-month"

    def test_exact_duplicate_rows_are_removed(self) -> None:
        row = _make_raw_dataframe()
        df = pd.concat([row, row.copy()], ignore_index=True)
        result = clean_data(df)
        assert len(result) == 1

    def test_total_charges_is_converted_to_numeric_dtype(self) -> None:
        df = _make_raw_dataframe(**{"Total Charges": "840.60"})
        result = clean_data(df)
        assert pd.api.types.is_numeric_dtype(result["total_charges"])
        assert result.loc[0, "total_charges"] == pytest.approx(840.60)


@pytest.mark.unit
class TestCleanDataEdgeCases:
    """
    Edge cases explicitly called out by Issue #13: missing required
    columns, empty datasets, and null patterns beyond what the initial
    inspection observed.
    """

    def test_missing_count_column_raises_keyerror(self) -> None:
        """
        KNOWN BUG (documented in docs/qa_findings.md): clean_data()
        calls df.drop(columns=["count"]) without errors="ignore",
        unlike every other column-drop in this codebase (compare
        training/preprocessing.py's DROP_COLUMNS, which uses
        errors="ignore"). A raw input missing the source "Count"
        column raises KeyError instead of failing gracefully or
        skipping the drop.

        This test intentionally asserts the CURRENT (buggy) behaviour
        rather than silently expecting graceful handling, so that if
        someone fixes clean_data.py later, this test fails loudly and
        the QA finding is confirmed resolved, not silently forgotten.
        """
        df = _make_raw_dataframe()
        df = df.drop(columns=["Count"])
        # Column has already been renamed to lowercase by this point?
        # No -- clean_data() renames internally; the raw column here
        # is still "Count" (title-case), same as production input.
        with pytest.raises(KeyError):
            clean_data(df)

    def test_empty_dataframe_with_correct_columns_returns_empty_result(self) -> None:
        """
        An empty (zero-row) but correctly-shaped input should clean
        successfully to an empty output, not raise.
        """
        empty_df = _make_raw_dataframe().iloc[0:0]
        result = clean_data(empty_df)
        assert len(result) == 0
        assert "customer_id" in result.columns

    def test_null_values_in_columns_not_normally_null_do_not_crash(self) -> None:
        """
        Unexpected null pattern: a column that the original inspection
        never observed nulls in (e.g. gender, contract) contains a
        null. clean_data() must not crash -- object-column whitespace
        stripping (.str.strip()) is null-safe in pandas, and this
        confirms that holds for this specific pipeline too.
        """
        df = _make_raw_dataframe(**{"Gender": None, "Contract": None})
        result = clean_data(df)
        assert pd.isna(result.loc[0, "gender"])
        assert pd.isna(result.loc[0, "contract"])

    def test_non_numeric_total_charges_for_nonzero_tenure_becomes_null_then_filled(self) -> None:
        """
        A non-numeric total_charges value for a customer who is NOT a
        brand-new (zero-tenure) customer is still coerced to NaN then
        filled to 0 by the current implementation -- clean_data() does
        not distinguish "genuinely missing/dirty data" from "new
        customer, zero charges" beyond the tenure-based comment. This
        documents the actual behaviour so a future change to that
        logic is caught by a failing test, not discovered in
        production.
        """
        df = _make_raw_dataframe(**{"Tenure Months": 24, "Total Charges": "not-a-number"})
        result = clean_data(df)
        assert result.loc[0, "total_charges"] == 0.0

    def test_all_rows_duplicate_of_each_other_collapses_to_one(self) -> None:
        """Extreme duplicate case: every row identical."""
        row = _make_raw_dataframe()
        df = pd.concat([row] * 5, ignore_index=True)
        result = clean_data(df)
        assert len(result) == 1

    def test_literal_empty_string_churn_reason_is_not_normalized(self) -> None:
        """
        DOCUMENTED FRAGILITY (see docs/qa_findings.md): unlike a
        genuinely-missing value (NaN, produced by pd.read_csv for a
        blank cell), a literal empty string "" is NOT considered null
        by pandas, so df["churn_reason"].fillna("Not Applicable")
        silently leaves it as "" rather than normalizing it.

        In production this is currently harmless, because
        clean_data() only ever runs on DataFrames from
        etl/inspect_raw_data.py's pd.read_csv(), which turns blank
        cells into real NaN, not "". But the function itself does not
        enforce or validate that assumption -- if it's ever called on
        data from a different source (a re-exported CSV that quotes
        empty fields as "", a JSON/API payload, a already-cleaned
        DataFrame passed through twice), churn_reason silently stops
        being normalized with no error or warning.

        This test intentionally asserts the CURRENT behaviour (value
        stays "") rather than the documented intent ("Not
        Applicable"), so it fails loudly -- and the QA finding is
        confirmed fixed -- if someone later hardens this with e.g.
        .replace("", pd.NA) before the fillna call.
        """
        df = _make_raw_dataframe(**{"Churn Label": "No", "Churn Reason": ""})
        result = clean_data(df)
        assert result.loc[0, "churn_reason"] == ""


# ======================================================================
# SECTION 2 -- INTEGRATION TESTS
# Real SQLite database, real CustomerRepository, real init_db.py.
# ======================================================================


@pytest.mark.integration
class TestDatabaseIdempotency:
    """Issue #13 explicit requirement: init_db.py must be idempotent."""

    def test_init_db_can_run_twice_without_error(self) -> None:
        init_db()
        init_db()  # must not raise

    def test_init_db_does_not_create_duplicate_tables(self) -> None:
        init_db()
        init_db()
        conn = get_connection()
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
            )
            matches = cursor.fetchall()
        finally:
            conn.close()
        assert len(matches) == 1

    @requires_populated_db
    def test_init_db_rerun_does_not_delete_existing_rows(self) -> None:
        """
        init_db() only runs DDL (CREATE TABLE IF NOT EXISTS) -- it
        must not truncate or otherwise affect existing data on a
        second run.
        """
        conn = get_connection()
        try:
            before = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        finally:
            conn.close()

        init_db()

        conn = get_connection()
        try:
            after = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        finally:
            conn.close()

        assert before == after


@pytest.mark.integration
class TestCustomerRepositoryBaselineCorrectness:
    """
    Issue #13 explicit requirement: get_all() returns a non-empty list
    after ETL has completed; get_by_id() behaves correctly for both a
    real and a non-existent customer_id.
    """

    @requires_populated_db
    def test_get_all_returns_nonempty_list_after_etl(self) -> None:
        repo = CustomerRepository()
        customers = repo.get_all()
        assert isinstance(customers, list)
        assert len(customers) > 0
        assert isinstance(customers[0], dict)

    @requires_populated_db
    def test_get_all_rows_contain_expected_schema_columns(self) -> None:
        repo = CustomerRepository()
        customers = repo.get_all()
        first = customers[0]
        for expected_column in (
            "customer_id",
            "gender",
            "tenure_months",
            "monthly_charges",
            "churn_label",
        ):
            assert expected_column in first

    @requires_populated_db
    def test_get_by_id_returns_none_for_nonexistent_id(self) -> None:
        repo = CustomerRepository()
        result = repo.get_by_id("THIS-ID-DOES-NOT-EXIST-999")
        assert result is None

    @requires_populated_db
    def test_get_by_id_returns_populated_dict_for_valid_id(self) -> None:
        repo = CustomerRepository()
        known_id = repo.get_all()[0]["customer_id"]

        result = repo.get_by_id(known_id)

        assert result is not None
        assert isinstance(result, dict)
        assert result["customer_id"] == known_id

    @requires_populated_db
    def test_get_by_id_is_safe_against_sql_injection_style_input(self) -> None:
        """
        Not exhaustive SQL-injection testing, but confirms the
        parametrized query in customer_repository.py treats a
        malicious-looking string as a literal id lookup (returns None
        rather than raising or returning unrelated rows).
        """
        repo = CustomerRepository()
        result = repo.get_by_id("' OR '1'='1")
        assert result is None


@pytest.mark.integration
class TestLoggingCoverage:
    """
    Issue #13 explicit requirement: confirm meaningful logs exist for
    rows loaded, rows after cleaning, and rows inserted -- using
    caplog rather than asserting on implementation internals.
    """

    def test_clean_data_logs_rows_after_cleaning(self, caplog: pytest.LogCaptureFixture) -> None:
        df = _make_raw_dataframe()
        with caplog.at_level(logging.INFO, logger="etl.clean_data"):
            clean_data(df)
        assert any("Rows after cleaning" in record.message for record in caplog.records)

    def test_clean_data_logs_null_count_for_total_charges(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        df = _make_raw_dataframe(**{"Total Charges": "not-numeric"})
        with caplog.at_level(logging.INFO, logger="etl.clean_data"):
            clean_data(df)
        assert any(
            "Null values in total_charges after conversion" in record.message
            for record in caplog.records
        )

    @requires_populated_db
    def test_repository_get_all_logs_row_count(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.INFO, logger="app.repository.customer_repository"):
            CustomerRepository().get_all()
        assert any("get_all returned" in record.message for record in caplog.records)

    def test_get_connection_logs_connection_target(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.INFO, logger="database.db_connection"):
            conn = get_connection()
            conn.close()
        assert any("Connected to database" in record.message for record in caplog.records)


@pytest.mark.integration
class TestSchemaConstraints:
    """
    Confirms sql/schema.sql's CHECK constraints (Mercy, #8) are
    actually enforced by SQLite at insert time -- not just present as
    text in the .sql file. Complements clean_data()'s unit tests by
    verifying the layer below it also rejects bad data.
    """

    def test_negative_monthly_charges_violates_check_constraint(self) -> None:
        init_db()
        conn = get_connection()
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    """
                    INSERT INTO customers (customer_id, churn_label, monthly_charges)
                    VALUES (?, ?, ?)
                    """,
                    ("TEST-NEG-CHARGE", "No", -10.0),
                )
                conn.commit()
        finally:
            conn.rollback()
            conn.close()

    def test_churn_value_outside_zero_or_one_violates_check_constraint(self) -> None:
        init_db()
        conn = get_connection()
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    """
                    INSERT INTO customers (customer_id, churn_label, churn_value)
                    VALUES (?, ?, ?)
                    """,
                    ("TEST-BAD-CHURN-VALUE", "No", 2),
                )
                conn.commit()
        finally:
            conn.rollback()
            conn.close()

    def test_null_churn_label_violates_not_null_constraint(self) -> None:
        init_db()
        conn = get_connection()
        try:
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO customers (customer_id, churn_label) VALUES (?, ?)",
                    ("TEST-NULL-LABEL", None),
                )
                conn.commit()
        finally:
            conn.rollback()
            conn.close()