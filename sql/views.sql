-- ==========================================================
-- SQL Views
--
-- Reusable analytical views for customer churn reporting.
--
-- These views depend on the customers table created in
-- sql/schema.sql.
-- ==========================================================

-- Business Question:
-- What is the churn rate by customer contract type?

CREATE VIEW IF NOT EXISTS view_churn_by_contract AS

SELECT
    contract,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN churn_label = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN churn_label = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate_percentage

FROM customers

GROUP BY contract;


-- Business Question:
-- What is the churn rate by customer tenure bucket?

CREATE VIEW IF NOT EXISTS view_churn_by_tenure_bucket AS

SELECT

    CASE
        WHEN tenure_months BETWEEN 0 AND 12 THEN '0-12 Months'
        WHEN tenure_months BETWEEN 13 AND 36 THEN '13-36 Months'
        ELSE '37+ Months'
    END AS tenure_bucket,

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN churn_label = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN churn_label = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate_percentage

FROM customers

GROUP BY tenure_bucket;