# SQL Analysis Summary

## Overview

This document summarizes the SQL analytics developed for **Issue #9** using the customer churn database created in **Issue #8**.

The analysis is based on the `customers` table in the SQLite database and includes exploratory SQL queries together with reusable analytical views for reporting and dashboard development.

---

# Analysis Queries

## 1. Overall Churn Rate

### Business Question

What percentage of customers have churned?

### Purpose

Calculates the overall customer churn rate to establish a baseline retention metric.

---

## 2. Churn Rate by Contract Type

### Business Question

How does churn differ across customer contract types?

### Purpose

Measures churn across Month-to-month, One year, and Two year contracts to understand the relationship between contract length and customer retention.

---

## 3. Churn Rate by Tenure Bucket

### Business Question

Which customer tenure group experiences the highest churn?

### Tenure Buckets

- 0–12 Months
- 13–36 Months
- 37+ Months

### Purpose

Segments customers by tenure to identify which lifecycle stages are most vulnerable to churn.

---

## 4. Average Monthly Charges

### Business Question

Do churned customers have different monthly charges compared with retained customers?

### Purpose

Compares average monthly charges for churned and retained customers to determine whether pricing is associated with customer attrition.

---

## 5. Feature Impact Analysis

### Business Question

Which service features have the greatest difference in churn rates between users and non-users?

### Purpose

Compares churn rates within customer subgroups using conditional aggregation to identify services associated with stronger customer retention.

---

# SQL Views

## view_churn_by_contract

### Purpose

Provides reusable contract-level churn metrics for reporting tools such as Power BI and Tableau.

### Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

## view_churn_by_tenure_bucket

### Purpose

Provides reusable tenure-based churn metrics for dashboards and business reporting.

### Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

# Validation

The SQL queries and analytical views were validated against the SQLite database generated through the ETL pipeline developed in Issue #8.

Validation included:

- Successful execution of all analytical queries
- Successful creation of SQL views
- Verification that analytical views return expected results
- Validation of feature-impact calculations using subgroup-specific churn rates

---

# Initial Findings

Initial analysis indicates:

- Overall customer churn is approximately **26.5%**.
- Month-to-month contracts experience the highest churn rates.
- Customers with shorter tenure are more likely to churn.
- Churned customers generally have higher monthly charges than retained customers.
- Service features such as **Online Security**, **Tech Support**, and **Online Backup** are associated with lower churn rates among subscribers.

> **Note:** Numerical results should be revalidated whenever the underlying dataset or ETL pipeline is updated.