-- Issue #8 -- ETL & Database -- sql/schema.sql
--
-- Column list and types derived from the real inspected dataset --
-- that part is Mercy's work and is unchanged. This pass only tightens
-- enforcement: NOT NULL where the data has no business being empty,
-- CHECK constraints matching what the original validate_data()
-- function already checked in Python (negative charges, churn_value
-- in {0,1}), and two type/column fixes below.

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY NOT NULL,

    -- "count" column dropped: it was a constant-1 utility column from
    -- the source Cognos export with no business meaning. Row counts
    -- are metadata (len(df) / SELECT COUNT(*)), not something to
    -- store per-row in the table itself -- especially redundant next
    -- to a primary key that already guarantees one row per customer.

    country TEXT,
    state TEXT,
    city TEXT,

    -- Changed from INTEGER to TEXT: a zip code is an identifier, not
    -- a quantity, and storing it as INTEGER silently drops leading
    -- zeros (00101 becomes 101). This also requires reading the
    -- column as a string at CSV-parse time in inspect_raw_data.py --
    -- fixed there too, since the type here alone doesn't help if the
    -- leading zero is already gone before this table ever sees it.
    zip_code TEXT,

    lat_long TEXT,  -- kept for fidelity to the source file, though it
                    -- duplicates latitude/longitude below -- worth
                    -- knowing these can drift out of sync with each
                    -- other since nothing enforces they match.
    latitude REAL CHECK (latitude BETWEEN -90 AND 90),
    longitude REAL CHECK (longitude BETWEEN -180 AND 180),

    gender TEXT,
    senior_citizen TEXT,
    partner TEXT,
    dependents TEXT,
    tenure_months INTEGER CHECK (tenure_months >= 0),
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
    monthly_charges REAL CHECK (monthly_charges >= 0),
    total_charges REAL CHECK (total_charges >= 0),

    -- NOT NULL: the issue itself requires this table to contain "the
    -- core customer entity and churn label" -- treating it as
    -- required, not optional.
    churn_label TEXT NOT NULL,

    churn_value INTEGER CHECK (churn_value IN (0, 1)),
    churn_score INTEGER CHECK (churn_score BETWEEN 0 AND 100),
    cltv INTEGER,
    churn_reason TEXT
);

-- No additional tables. All inspected columns describe a single
-- customer and belong directly on customers.