# Customer Churn Prediction & Business Intelligence Platform

An end-to-end analytics platform that helps organizations identify customers at risk of churn, understand the factors driving customer loss, and make data-driven retention decisions through machine learning, APIs, SQL analytics, and interactive dashboards.

## Project Overview

Customer churn is a major challenge for subscription-based businesses such as telecom providers and financial institutions. This project builds a production-style churn analytics platform that combines:

- Data engineering pipelines
- Database design
- Exploratory data analysis
- Feature engineering
- Machine learning prediction
- REST API deployment
- Business intelligence dashboards

The final solution enables stakeholders to:

- Identify customers likely to churn
- Understand key churn drivers
- Estimate potential revenue impact
- Generate actionable retention recommendations

---

# Objectives

The main objectives of this project are:

1. Build a complete data pipeline from raw data ingestion to analytics.
2. Clean and transform customer data for machine learning.
3. Develop classification models to predict customer churn.
4. Expose predictions through a FastAPI service.
5. Create business intelligence dashboards for decision-making.
6. Practice professional software engineering workflows including Git, code reviews, testing, and documentation.

---

# Dataset

The project uses the following customer churn datasets:

- IBM Telco Customer Churn Dataset

This dataset contains:

- Missing values
- Categorical variables
- Customer demographics
- Business KPIs
- Binary classification target (Churn / No Churn)

---

# System Architecture

```

CSV Dataset
|
▼
ETL Pipeline
|
▼
Clean Database
(SQLite / PostgreSQL)
|
├──────────────► SQL Analysis
|
▼
Feature Engineering
|
▼
Model Training
|
▼
Prediction Service
|
▼
FastAPI Application
|
▼
Power BI Dashboard

```

---

# Technology Stack

## Data Engineering
- Python
- Pandas
- SQL
- SQLite 

## Machine Learning
- Scikit-learn
- XGBoost (optional)
- Joblib / Pickle for model persistence

## Backend
- FastAPI
- Pydantic
- Uvicorn

## Analytics & Visualization
- Power BI
- SQL Analytics

## Development Practices
- GitHub Issues
- Feature Branch Workflow
- Pull Requests
- Code Reviews
- Unit Testing
- Documentation

---

# Project Timeline

## Sprint 1: Data, Analytics & Modeling

### Data Engineering

Tasks:

- Import dataset
- Clean missing values
- Perform validation checks
- Create database tables
- Build ETL pipeline

Deliverables:

```

etl/
database/
repository/
sql/

```

---

### Exploratory Data Analysis

Tasks:

- Analyze customer demographics
- Identify churn patterns
- Calculate business KPIs
- Generate insights

---

### Machine Learning

Models:

- Logistic Regression
- Random Forest
- XGBoost (optional)

Evaluation metrics:

- Accuracy
- Precision
- Recall
- ROC-AUC
- Confusion Matrix

The best-performing model will be selected and persisted for production use.

Deliverables:

```

models/
training/
evaluation/
predict.py

```

---

## Sprint 2: API, Dashboard & Integration

### FastAPI Prediction Service

The API provides access to customer information, business metrics, and churn predictions.

Endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Check API status |
| `/customers` | GET | Retrieve customer records |
| `/kpis` | GET | Retrieve business KPIs |
| `/predict` | POST | Generate churn prediction |
| `/model-metrics` | GET | Retrieve model performance metrics |

Deliverables:

```

api/
services/
schemas/

```

---

# Power BI Dashboard

The dashboard provides business-facing insights through multiple pages:

## Executive Overview
- Total customers
- Churn rate
- Revenue impact
- High-level business KPIs

## Customer Demographics
- Customer segments
- Age groups
- Geographic analysis

## Churn Drivers
- Factors influencing churn
- Contract analysis
- Service usage patterns

## Revenue Impact
- Lost revenue estimation
- Customer value analysis

## Model Predictions
- Customers at high churn risk
- Prediction probabilities
- Retention opportunities

Deliverables:

```

dashboard/
business_report.md

```

---

# Repository Structure

```

customer-churn-platform/
├── app/
│   ├── api/
│   ├── models/
│   ├── repository/
│   └── services/
├── dashboard/
│   └── business_report.md
├── database/
├── docs/
│   └── data_dictionary.md
├── etl/
├── evaluation/
├── schemas/
├── sql/
├── tests/
│   ├── test_api.py
│   ├── test_etl.py
│   └── test_models.py
├── training/
├── utils/
├── data/
├── predict.py
└── README.md

```

---

# Team Structure

## Project Lead
### Theresia

Responsibilities:

- Sprint planning
- Creating and managing GitHub Issues
- Task allocation
- Standups
- Repository standards
- Folder structure
- Documentation quality
- Final integration
- Presentation coordination
- Deadline management

---

## Data Engineering Lead
### Mercy

Responsibilities:

- Data ingestion
- ETL pipeline
- Data validation
- Database design
- SQL schema
- Repository layer

Deliverables:

```

etl/
database/
repository/
sql/

```

---

## Machine Learning Lead
### Latifah

Responsibilities:

- Feature engineering
- Model training
- Model evaluation
- Model persistence
- Prediction utilities

Deliverables:

```

models/
training/
evaluation/
predict.py

```

---

## Backend/API Engineer
### Praise

Responsibilities:

- FastAPI implementation
- API routes
- Dependency injection
- Services
- Model serving

Deliverables:

```

api/
services/
schemas/

```

---

## Business Intelligence Lead
### Joyce

Responsibilities:

- Exploratory analysis
- Business insights
- KPI definition
- Power BI dashboard
- Recommendations

Deliverables:

```

dashboard/
business_report.md

```

---

## Testing & QA Lead
### Pamela

Responsibilities:

- Unit testing
- Integration testing
- Edge-case testing
- Logging verification
- Bug reporting

Deliverables:

```

tests/
test_api.py
test_models.py
test_etl.py

```

---

## Data Analyst & Documentation Lead
### Salome

Responsibilities:

- SQL analysis
- Data dictionary
- Documentation
- README maintenance
- API examples
- Business interpretation

Deliverables:

```

README.md
docs/
data_dictionary.md

```

---

# Git Workflow

All development follows a feature-based workflow:

```

Issue
↓
Feature Branch
↓
Development
↓
Pull Request
↓
Code Review
↓
Merge

```

## Rules

- No direct pushes to `main`.
- Every feature must have a GitHub Issue.
- Every PR must:
  - Reference the related issue
  - Receive review approval
  - Pass CI checks
  - Pass tests before merging

Pull request reviews will be coordinated by the project leads.

---

# Definition of Done

A task is considered complete only when:

✅ Code works as expected  
✅ Tests are included  
✅ Type hints are added  
✅ Logging is implemented where required  
✅ Documentation is updated  
✅ Pull request is approved  
✅ Changes are merged into `main`

---

# Testing Strategy

Testing covers:

- ETL pipeline validation
- API endpoint functionality
- Model prediction behavior
- Edge cases and invalid inputs

Test structure:

```

tests/

├── test_api.py
├── test_models.py
└── test_etl.py

```

---

# Stretch Goals

If the core project is completed early:

- SHAP explainability
- Docker containerization
- GitHub Actions CI/CD
- Cloud deployment
- PostgreSQL migration
- Streamlit demonstration application

---

# Learning Outcomes

This project focuses on more than building a churn prediction model. It provides practical experience with professional software development practices.

By completing this project, the team will practice:

- Breaking large projects into manageable tasks
- Collaborating through GitHub workflows
- Developing modular and maintainable code
- Writing tests and documentation
- Reviewing code through pull requests
- Integrating independently developed components
- Delivering a production-style analytics application

---

# Contributors

| Name | Role |
|---|---|
| Theresia | Project Lead |
| Mercy | Data Engineering |
| Latifah | Machine Learning |
| Praise | Backend/API |
| Joyce | Business Intelligence |
| Pamela | QA & Testing |
| Salome | Documentation & Analysis |

---

# License

This project is for educational and portfolio purposes.
```

I would recommend adding a small **"Screenshots / Demo"** section after the Power BI dashboard is complete because this type of project benefits heavily from visual proof on GitHub.
