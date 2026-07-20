# Data Dictionary

> **Status:** Draft – Pending final confirmation after Issue #8 (SQLite schema) is merged into `main`.

## Overview

This document describes the fields used in the Customer Churn dataset and the business meaning of each column. The final data types and constraints will be verified against the finalized SQLite schema after Issue #8 is merged.

**Dataset**

IBM Telco Customer Churn Dataset

**Primary Table (Current Draft)**

`customer_churn`

> **Note**
>
> After Issue #8 is merged, references to `customer_churn` will be updated to the production table (`customers`) if required.

---

## Column Dictionary

| Column | Description | Example |
|---------|-------------|---------|
| Customer ID | Unique identifier for each customer | 7590-VHVEG |
| Gender | Customer gender | Male, Female |
| Senior Citizen | Indicates whether the customer is a senior citizen | Yes / No |
| Partner | Whether the customer has a partner | Yes / No |
| Dependents | Whether the customer has dependents | Yes / No |
| Tenure Months | Number of months the customer has remained with the company | 24 |
| Phone Service | Whether phone service is subscribed | Yes / No |
| Multiple Lines | Whether customer has multiple phone lines | Yes / No |
| Internet Service | Type of internet service | DSL, Fiber Optic, No |
| Online Security | Whether online security service is subscribed | Yes / No |
| Online Backup | Whether online backup service is subscribed | Yes / No |
| Device Protection | Whether device protection is subscribed | Yes / No |
| Tech Support | Whether technical support service is subscribed | Yes / No |
| Streaming TV | Whether streaming TV service is subscribed | Yes / No |
| Streaming Movies | Whether streaming movie service is subscribed | Yes / No |
| Contract | Customer contract type | Month-to-month, One year, Two year |
| Paperless Billing | Whether paperless billing is enabled | Yes / No |
| Payment Method | Customer payment method | Electronic Check, Bank Transfer, Credit Card, Mailed Check |
| Monthly Charges | Monthly service charge | 75.30 |
| Total Charges | Total amount charged to the customer | 2045.60 |
| Churn Label | Indicates whether the customer churned | Yes / No |

---

## SQL Views

The project currently exposes the following analytical views.

### view_churn_by_contract

Purpose

Calculates customer churn metrics grouped by contract type.

Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

### view_churn_by_tenure_bucket

Purpose

Calculates churn metrics across tenure groups.

Buckets

- 0–12 Months
- 13–36 Months
- 37+ Months

Metrics

- Total customers
- Churned customers
- Churn rate (%)

---

## Pending Items

The following items will be confirmed after Issue #8 is merged.

- Final SQLite table name
- SQLite column data types
- Primary key
- Constraints
- Foreign keys (if introduced)