-- ==========================================================
-- Customer Churn Analysis Queries
-- Temporary table: customer_churn
-- Based on Telco_customer_churn.xlsx dataset
-- ==========================================================


-- Business Question:
-- What percentage of customers have churned?

SELECT
    ROUND(
        100.0 * SUM(CASE WHEN "Churn Label" = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customer_churn;



-- Business Question:
-- How does churn rate differ across customer contract types?

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN "Churn Label" = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 *
        SUM(CASE WHEN "Churn Label" = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_percentage DESC;



-- Business Question:
-- Which customer tenure group has the highest churn rate?

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
    / COUNT(*),
    2
) AS churn_rate_percentage

FROM customer_churn

GROUP BY tenure_bucket

ORDER BY churn_rate_percentage DESC;



-- Business Question:
-- Do churned customers have different average monthly charges compared with retained customers?

SELECT

"Churn Label",

ROUND(
    AVG("Monthly Charges"),
    2
) AS average_monthly_charges

FROM customer_churn

GROUP BY "Churn Label";



-- Business Question:
-- Which services/features have the largest difference in churn rate between users and non-users?


WITH feature_churn AS (

SELECT
    'Online Security' AS feature,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Online Security"='Yes'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Online Security"='Yes'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    ) AS users_churn_rate,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Online Security"='No'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Online Security"='No'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    ) AS non_users_churn_rate

FROM customer_churn

UNION ALL

SELECT
    'Tech Support',

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Tech Support"='Yes'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Tech Support"='Yes'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    ),

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Tech Support"='No'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Tech Support"='No'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    )

FROM customer_churn

UNION ALL

SELECT
    'Online Backup',

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Online Backup"='Yes'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Online Backup"='Yes'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    ),

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN "Online Backup"='No'
                 AND "Churn Label"='Yes'
                THEN 1 ELSE 0
            END
        )
        /
        NULLIF(
            SUM(
                CASE
                    WHEN "Online Backup"='No'
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        2
    )

FROM customer_churn

)

SELECT

    feature,
    users_churn_rate AS users_churn_percentage,
    non_users_churn_rate AS non_users_churn_percentage,
    ROUND(
        ABS(users_churn_rate - non_users_churn_rate),
        2
    ) AS churn_difference

FROM feature_churn

ORDER BY churn_difference DESC

LIMIT 3;