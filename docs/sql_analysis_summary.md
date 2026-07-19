# SQL Analysis Summary

## Overview

This document explains the SQL analytics queries and views created for Issue #9.

The analysis is currently tested using the Telco customer churn dataset loaded into a temporary SQLite table called `customer_churn`.

---

# Analysis Queries

## 1. Overall Churn Rate

### Business Question
What percentage of customers have churned?

### Purpose
Calculates the overall percentage of customers who left the service.

---

## 2. Churn Rate by Contract Type

### Business Question
How does churn differ across contract types?

### Purpose
Identifies whether customers with different contract commitments have different churn behavior.

---

## 3. Churn Rate by Tenure Bucket

### Business Question
Which customer tenure group experiences the highest churn?

### Groups

- 0–12 months
- 13–36 months
- 37+ months

### Purpose
Shows whether newer or longer-term customers are more likely to leave.

---

## 4. Average Monthly Charges

### Business Question
Do churned customers have different monthly charges compared with retained customers?

### Purpose
Compares average monthly spending between churned and active customers.

---

## 5. Feature Impact Analysis

### Business Question
Which services have the largest churn difference between users and non-users?

### Purpose
Identifies services that may influence customer retention.

---

# SQL Views

## view_churn_by_contract

### Business Question
What is the churn rate for each contract type?

### Purpose
Provides Power BI with contract-level churn metrics.

---

## view_churn_by_tenure_bucket

### Business Question
How does churn vary by customer tenure?

### Purpose
Provides Power BI with tenure-based churn segmentation.

---

# Current Status

Final SQL views will be updated after Mercy's SQLite schema is merged.

# Initial Findings From Local Testing

The SQL queries were tested using the Telco customer churn dataset loaded into an in-memory SQLite database.

# Key observations:

- Overall churn rate is approximately **26.54%** of customers.
- Month-to-month contracts represent the largest customer group with **3,875 customers**.
- Churned customers have higher average monthly charges (**74.44**) compared with retained customers (**61.27**).