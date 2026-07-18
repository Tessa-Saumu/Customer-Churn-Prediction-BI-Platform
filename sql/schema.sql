-- Issue #8 -- ETL & Database -- sql/schema.sql
--
-- IMPORTANT: this must be derived from the ACTUAL columns in
-- data/raw/telco_churn_raw.csv, not from general knowledge of "the
-- Telco churn dataset." This version has extra columns (Churn Score,
-- CLTV, Churn Reason, and possibly others) beyond the commonly-cited
-- 21-feature version. The project spec explicitly says to reject any
-- PR that assumes a schema instead of deriving it from the real file --
-- so before filling this in, re-run etl/inspect_raw_data.py and work
-- from its real column list and dtypes, one by one.
--
-- Process to follow:
--   1. Run etl/inspect_raw_data.py, get the real column list + dtypes.
--   2. For each column: does it belong directly on customers, or does
--      it represent a genuine one-to-many relationship that deserves
--      its own table? Most columns here will belong directly on
--      customers -- don't over-normalize under today's time pressure.
--      Only split out a table if there's an actual repeating group.
--   3. Map pandas dtypes to SQL types: object/string -> TEXT,
--      int64 -> INTEGER, float64 -> REAL.
--   4. Every table must use CREATE TABLE IF NOT EXISTS --
--      database/init_db.py running twice without error is an
--      acceptance criterion, and that's enforced here, not there.
--
-- customer_id is the one column safe to commit to already, since
-- CustomerRepository.get_by_id(customer_id: str) already depends on it
-- existing as the primary key. Confirm the exact raw column name from
-- your inspect output (likely "CustomerID" before standardization) and
-- adjust the name below if it differs.

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    
    count INTEGER,

    country TEXT,

    state TEXT,

    city TEXT,

    zip_code INTEGER,

    lat_long TEXT,

    latitude REAL,

    longitude REAL,

    gender TEXT,

    senior_citizen TEXT,

    partner TEXT,

    dependents TEXT,

    tenure_months INTEGER,

    phone_service TEXT,

    multiple_lines TEXT,

    internet_service TEXT,

    online_security TEXT,

    online_backup TEXT,

    device_protection TEXT,

    tech_support TEXT,

    streaming_tv TEXT,

    streaming_movies TEXT,

    contract TEXT,

    paperless_billing TEXT,

    payment_method TEXT,

    monthly_charges REAL,

    total_charges REAL,

    churn_label TEXT,

    churn_value INTEGER,

    churn_score INTEGER,

    cltv INTEGER,

    churn_reason TEXT

);

-- No additional tables were created.
-- All inspected columns describe a single customer and belong
-- directly to the customers table.