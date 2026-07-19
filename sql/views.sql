-- ==========================================================
-- Draft SQL Views
--
-- These views currently use the temporary table:
-- customer_churn
--
-- They must be updated after Mercy's final SQLite schema
-- is merged.
-- ==========================================================


-- Business Question:
-- What is the churn rate by customer contract type?

CREATE VIEW view_churn_by_contract AS

SELECT

Contract,

COUNT(*) AS total_customers,

SUM(
CASE WHEN "Churn Label"='Yes'
THEN 1 ELSE 0 END
) AS churned_customers,

ROUND(
100.0 *
SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END)
/
COUNT(*),
2
) AS churn_rate_percentage

FROM customer_churn

GROUP BY Contract;



-- Business Question:
-- What is the churn rate by customer tenure bucket?

CREATE VIEW view_churn_by_tenure_bucket AS

SELECT

CASE
    WHEN "Tenure Months" BETWEEN 0 AND 12 THEN '0-12 Months'
    WHEN "Tenure Months" BETWEEN 13 AND 36 THEN '13-36 Months'
    ELSE '37+ Months'
END AS tenure_bucket,


COUNT(*) AS total_customers,


SUM(
CASE WHEN "Churn Label"='Yes'
THEN 1 ELSE 0 END
) AS churned_customers,


ROUND(
100.0 *
SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END)
/
COUNT(*),
2
) AS churn_rate_percentage


FROM customer_churn

GROUP BY tenure_bucket;