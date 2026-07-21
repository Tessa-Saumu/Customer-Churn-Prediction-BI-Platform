# Data Dictionary

> **Status:** Updated based on the merged SQLite schema (`customers` table). This document describes the customer attributes used throughout the ETL pipeline, SQL analysis, and BI reporting.

---

# Overview

The Customer Churn dataset contains demographic, geographic, service subscription, billing, and churn information for customers. These fields support SQL analytics, business intelligence dashboards, and customer churn prediction.

**Dataset**

IBM Telco Customer Churn Dataset

**Primary Table**

`customers`

---

# Column Dictionary

| Column | SQLite Type | Description | Example | Why it may relate to churn |
|---------|-------------|-------------|---------|----------------------------|
| customer_id | TEXT | Unique identifier for each customer. Primary key. | 7590-VHVEG | Used to uniquely identify each customer record. |
| country | TEXT | Country where the customer resides. | United States | Customer behaviour may differ by country. |
| state | TEXT | State of residence. | California | Regional differences may influence churn patterns. |
| city | TEXT | Customer city. | Los Angeles | Enables geographic churn analysis. |
| zip_code | TEXT | Postal/ZIP code. | 90001 | Supports regional segmentation. |
| lat_long | TEXT | Combined latitude and longitude coordinates. | 34.05,-118.24 | Supports mapping and geographic visualization. |
| latitude | REAL | Latitude coordinate. | 34.05 | Used for geographic analysis. |
| longitude | REAL | Longitude coordinate. | -118.24 | Used for geographic analysis. |
| gender | TEXT | Customer gender. | Male | Demographic feature for segmentation. |
| senior_citizen | TEXT | Indicates whether the customer is a senior citizen. | Yes | Senior customers may have different retention behaviour. |
| partner | TEXT | Indicates whether the customer has a partner. | Yes | Household composition may influence retention. |
| dependents | TEXT | Indicates whether the customer has dependents. | No | Family responsibilities may affect customer loyalty. |
| tenure_months | INTEGER | Number of months the customer has remained with the company. | 24 | One of the strongest predictors of churn. |
| phone_service | TEXT | Indicates whether phone service is subscribed. | Yes | Service adoption may influence churn. |
| multiple_lines | TEXT | Indicates whether multiple phone lines are subscribed. | No | Reflects service usage complexity. |
| internet_service | TEXT | Type of internet service. | Fiber optic | Internet technology often correlates with churn. |
| online_security | TEXT | Indicates whether online security service is subscribed. | Yes | Value-added services may improve customer retention. |
| online_backup | TEXT | Indicates whether online backup service is subscribed. | No | Additional services may reduce churn. |
| device_protection | TEXT | Indicates whether device protection is subscribed. | Yes | Customers using more services often remain longer. |
| tech_support | TEXT | Indicates whether technical support is subscribed. | Yes | Better support can reduce customer dissatisfaction. |
| streaming_tv | TEXT | Indicates whether streaming TV is subscribed. | Yes | Entertainment services may increase engagement. |
| streaming_movies | TEXT | Indicates whether streaming movies are subscribed. | No | Higher service adoption may improve retention. |
| contract | TEXT | Customer contract type. | Month-to-month | One of the strongest churn indicators. |
| paperless_billing | TEXT | Indicates whether paperless billing is enabled. | Yes | Billing preferences may relate to customer behaviour. |
| payment_method | TEXT | Customer payment method. | Electronic check | Certain payment methods show higher churn rates. |
| monthly_charges | REAL | Monthly service charges. | 75.30 | Higher monthly charges may increase churn risk. |
| total_charges | REAL | Total amount paid by the customer. | 2045.60 | Indicates long-term customer value. |
| churn_label | TEXT | Indicates whether the customer churned. | Yes | Primary target variable for churn analysis. |
| churn_value | INTEGER | Binary churn indicator (0 = No, 1 = Yes). | 1 | Machine-learning friendly representation of churn. |
| churn_score | INTEGER | Estimated churn risk score. | 82 | Indicates predicted likelihood of churn. |
| cltv | INTEGER | Customer Lifetime Value. | 4500 | High-value customers are important for retention strategies. |
| churn_reason | TEXT | Reported reason for customer churn. | Competitor offered better service | Helps identify business drivers of customer loss. |

---

# SQL Views

## view_churn_by_contract

### Purpose

Summarizes customer churn metrics by contract type.

### Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

## view_churn_by_tenure_bucket

### Purpose

Summarizes customer churn across tenure groups.

### Buckets

- 0–12 Months
- 13–36 Months
- 37+ Months

### Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

# Notes

- This document reflects the merged SQLite schema (`customers` table).
- Column names follow the standardized snake_case naming convention used throughout the ETL pipeline.
- The SQL views support downstream analytics and business intelligence reporting.