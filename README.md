# Customer Churn Prediction & Business Intelligence Platform

An end-to-end analytics platform that identifies customers likely to churn and surfaces actionable recommendations through a Power BI dashboard and a FastAPI service.

**Timeline:** 9-day target (mentor ceiling: 14 days)
**Dataset:** [IBM Telco Customer Churn — Cognos Analytics version](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Git Workflow](#git-workflow)
3. [Pull Request Template](#pull-request-template)
4. [Definition of Done](#definition-of-done)
5. [Repository Structure](#repository-structure)
6. [Architecture](#architecture)
7. [Team & Responsibilities](#team--responsibilities)
8. [Review Process](#review-process)
9. [Sprint Board](#sprint-board)
10. [Milestones](#milestones)
11. [Running the Project](#running-the-project)
12. [Stretch Goals](#stretch-goals)

---

## Getting Started

### Prerequisites

- **Git** — [install instructions](https://git-scm.com/downloads)
- **Python 3.12** — confirm with `python --version`
- A GitHub account added as a collaborator on this repository

### Clone the repository

```bash
git clone https://github.com/Tessa-Saumu/Customer-Churn-Prediction-BI-Platform.git
cd Customer-Churn-Prediction-BI-Platform
```

### Set up your local environment

```bash
# Confirm git is installed
git --version

# Configure your git identity (one-time, if not already done)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Confirm Python 3.12 is installed
python --version

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure environment variables

Copy the example environment file and fill in real values:

```bash
cp .env.example .env
```

See `.env.example` for the full list of required variables (API key, database path, etc.). **Never commit `.env`** — it's already listed in `.gitignore`.

As of Issue #14 (real model integration), two additional variables are supported. Both are optional -- if unset, they default to the repo-standard paths (models/best_model.pkl and evaluation/model_comparison.md), so no .env change is required to run the project as before. Set them only if your model artifacts live somewhere other than the repo root (e.g. a container image that copies only app/, predict.py, and models/):

MODEL_PATH=models/best_model.pkl
MODEL_METRICS_PATH=evaluation/model_comparison.md

---

## Git Workflow

**No direct pushes to `main`. Ever.** Every change — no matter how small — follows this sequence:

```
Issue → Branch → Development → Pull Request → Code Review → Final Review (Michael) → Merge
```

### Branch naming

Use the format `<your-name>/<short-description>`, all lowercase, words separated by hyphens:

```bash
git checkout -b mercy/etl-schema
git checkout -b praise/fastapi-scaffold
```

### Making changes

```bash
# Make sure main is up to date before branching
git checkout main
git pull origin main

# Create your branch
git checkout -b <your-name>/<short-description>

# ... make your changes ...

# Stage and commit
git add <files>
git commit -m "type: short description of what changed"

# Push your branch
git push origin <your-name>/<short-description>
```

### Commit message convention

Prefix commits with a type, followed by a short, present-tense description:

- `feat:` — a new feature (e.g. `feat: add customer repository layer`)
- `fix:` — a bug fix
- `chore:` — setup, tooling, or non-feature changes
- `docs:` — documentation-only changes
- `test:` — adding or updating tests

### Opening a Pull Request

1. Push your branch to GitHub.
2. Open a Pull Request targeting `main`.
3. Use the [PR template](#pull-request-template) below — copy it in full, don't skip sections.
4. Link the PR to its issue using `Closes #<issue-number>` in the "Related Issue" section.
5. Request review.
6. Once your PR is open, post a completion comment on the linked issue:

   ```markdown
   PR opened to address this issue: #<PR-number>.
   <Short summary of what was completed — 1 sentence>
   All changes have been implemented and verified locally.
   ```

**If what you actually built differs at all from the issue's original scope** — a renamed function, a different library, an extra endpoint you thought was needed — call this out explicitly under "Notes" in the PR description and flag it for confirmation. Do not silently ship a deviation, even one you believe is an improvement.

---

## Pull Request Template

Copy this in full into every PR description:

```markdown
## Summary
Briefly describe what this PR does and why it exists.
(1–2 sentences, outcome-focused)

## Scope
What is included in this PR:
- 
- 
- 

## Implementation Details
Key technical work completed:
- 
- 
- 

## Validation / Testing
How you verified this works:
- 
- 
- 

## Configuration / Setup Changes (if applicable)
- Environment variables:
- New dependencies:
- Migrations / schema updates:

## Notes
Anything reviewers should be aware of:
- 
- 

## Related Issue
Closes #<issue-number>

## How to Run (if relevant)
Steps to reproduce or run locally:
​```bash
# example
python -m scripts.init_db
​```
```

---

## Definition of Done

A task is complete only if:

- Code works
- Tests added
- Type hints included (Python's `typing` module / built-in generics — no untyped function signatures)
- Logging included (`logging` module — no `print()` statements)
- Documentation updated
- PR approved by Theresia (first-pass review)
- Signed off by Michael (final review — required on **every** PR before merge)
- Merged into `main`

---

## Repository Structure

```
customer-churn-platform/
├── app/
│   ├── api/           # FastAPI route definitions
│   ├── models/        # Trained model artifacts / model-related classes
│   ├── repository/    # Data access layer (queries the database)
│   └── services/       # Business logic, auth, prediction services
├── dashboard/
│   └── business_report.md
├── database/           # SQLite connection logic, DB init scripts, the .db file (gitignored)
├── docs/
│   └── data_dictionary.md
├── etl/                 # Data ingestion and cleaning scripts
├── evaluation/          # Model evaluation scripts and metrics
├── schemas/             # Pydantic request/response schemas
├── sql/                 # Schema DDL, analysis queries, views
├── tests/
│   ├── test_api.py
│   ├── test_etl.py
│   └── test_models.py
├── training/            # Model training scripts
├── utils/               # Shared helper functions
├── data/
│   └── raw/             # Raw dataset CSV (gitignored — see .gitignore)
├── predict.py           # Prediction entry point
├── .env.example
├── .gitignore
└── README.md
```

---

## Architecture

```
CSV
 │
 ▼
ETL Pipeline
 │
 ▼
Clean Database (SQLite)
 │
 ├─────────────► SQL Analysis (views + queries)
 │
 ▼
Feature Engineering
 │
 ▼
Model Training (5 models)
 │
 ▼
Prediction Service
 │
 ▼
FastAPI (5 endpoints, API key auth)
 │
 ▼
Power BI Dashboard (connected via ODBC)
```

### Models

Five models are trained and compared: **Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM.** Evaluation metrics: Accuracy, Precision, Recall, ROC AUC, Confusion Matrix. Best model is selected and used for the `/predict` endpoint.

### Feature Engineering

Before model training, the preprocessing pipeline generates three derived features:

- **TenureBucket** – Groups customers into tenure ranges (0–12, 13–24, 25–48 and 49+ months).
- **TotalServicesCount** – Counts the number of subscribed services for each customer.
- **AvgMonthlySpend** – Calculates the customer's average monthly spend using total charges and tenure.

These engineered features are created dynamically during preprocessing and are not stored in the SQLite database.

### API Endpoints

All endpoints require an `X-API-Key` header except `/health`.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Health check, no auth |
| `/customers` | GET | Returns customer records |
| `/kpis` | GET | Returns business KPIs |
| `/predict` | POST | Returns a churn prediction for a given customer |
| `/model-metrics` | GET | Returns the best model's evaluation metrics |

### Dashboard

Power BI, connected to `database/churn.db` via an **ODBC driver** (install the SQLite ODBC driver, configure a DSN pointing at the database file, then connect Power BI using that DSN). Pages:

- Executive Overview
- Customer Demographics
- Churn Drivers
- Revenue Impact
- Model Predictions

---

## Team & Responsibilities

| Name | Role | Deliverables |
|---|---|---|
| **Theresia** | Team Lead | Sprint planning, GitHub issues, board maintenance, standups, coding standards, final integration, presentation coordination |
| **Mercy** | Lead Data Engineer | `etl/`, `database/`, `repository/`, `sql/` |
| **Latifah** | Lead ML Engineer | `models/`, `training/`, `evaluation/`, `predict.py` |
| **Praise** | Backend/API Engineer | `api/`, `services/`, `schemas/` |
| **Joyce** | Lead BI & Analytics | `dashboard/`, `business_report.md` |
| **Pamela** | Lead Testing & QA | `tests/`, `test_api.py`, `test_models.py`, `test_etl.py` |
| **Salome** | Lead Data Analyst & Documentation | `README.md`, `docs/`, `data_dictionary.md` |

**Coordination note:** Joyce and Salome must stay in sync — the dashboard connects directly to the SQL views Salome produces, so any change to view names or structure should be communicated directly, not left to surface at standup.

---

## Review Process

Every PR follows a two-step gate:

1. **First-pass review** — Theresia reviews for correctness, adherence to the Definition of Done, and scope alignment.
2. **Final sign-off** — Michael reviews and signs off on **every individual PR** before it can merge. This is a hard, per-PR gate, not a milestone-level check.

Given the compressed timeline, keep PRs small and scoped to a single issue — this keeps both review passes fast.

---

## Sprint Board (Click on the Projects Tab)

GitHub Projects board with these columns, in order:

**Backlog → To Do → In Progress → In Review → Changes Requested → Final Review (Michael) → Done**

- **Backlog:** everything identified as needed for the project, including work not yet unblocked.
- **To Do:** the subset of Backlog that's unblocked and ready to be picked up right now.
- **In Review:** open PR, awaiting Theresia's pass.
- **Changes Requested:** sent back after review; move back to In Review once addressed.
- **Final Review (Michael):** passed first review, awaiting Michael's sign-off.
- **Done:** merged into `main`.

---

## Milestones

| Milestone | Covers |
|---|---|
| **M0: Sprint Kickoff** | Repository setup & onboarding, all team members |
| **M1: Data Foundation** | ETL, database, schema, SQL analysis, views |
| **M2: API Scaffold** | FastAPI application shell with mocked prediction |
| **M3: Model Training** | 5-model training, evaluation, `predict.py` |
| **M4: Real Integration** | Swap mocked prediction for real model; full test suite against real components |
| **M5: Dashboard** | Power BI, ODBC connection, all 5 pages |
| **M6: Docs, Testing Polish & Presentation** | Final documentation, full test pass, presentation prep |
| **M7 (optional): Stretch Goals** | Owned by Michael — only pursued if the core milestones finish early |

---

## Running the Project
This section demonstrates how to run the project;the set of instructions are given in the following sections below:
### Run the machine learning training pipeline

After the ETL pipeline has loaded the customer data into the database, install the project dependencies (if you have not already done so):

```bash
pip install -r requirements.txt
```

Run the complete model training and evaluation pipeline:

```bash
python training/evaluate_models.py
```

This command will:

- Train all five machine learning models:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - XGBoost
  - LightGBM
- Evaluate each model using Accuracy, Precision, Recall, ROC AUC, and a Confusion Matrix.
- Select the best-performing model based on the evaluation metrics.
- Save the selected model to `models/best_model.pkl`.
- Generate the evaluation report at `evaluation/model_comparison.md`.

### Run the ETL pipeline

```bash
python database/init_db.py
python etl/load_to_db.py
python database/init_views.py
```

### Run the API locally

Before running the API (as of Issue #14): /predict and /model-metrics now call real artifacts instead of placeholders, so both must exist first:

models/best_model.pkl — produced by training/evaluate_models.py (see Run the machine learning training pipeline above). /predict will fail to start if this file is missing.
evaluation/model_comparison.md — also produced by training/evaluate_models.py. /model-metrics returns a 500 with a clear error message if this file is missing, rather than failing silently or falling back to placeholder numbers.

/customers and /kpis require the database to be initialized and populated first — i.e. the Run the ETL pipeline steps must have already been completed at least once.

In short, as of Issue #14 the full local startup order is:

```bash
# 1. ETL — populates database/churn.db
python database/init_db.py
python etl/load_to_db.py
python database/init_views.py

# 2. Training — populates models/best_model.pkl and
#    evaluation/model_comparison.md
python training/evaluate_models.py

# 3. API — now backed entirely by real data/model from steps 1-2
uvicorn app.main:app --reload
```

Then, in a separate terminal, verify all 5 endpoints:

**macOS / Linux:**
```bash
API_KEY=<your-key-from-.env> ./scripts/verify_endpoints.sh
```

**Windows (PowerShell):**
```powershell
$env:API_KEY="<your-key-from-.env>"; ./scripts/verify_endpoints.ps1
```

Both scripts check `/health` (no auth), `/customers`, `/kpis`, `/model-metrics`, and `/predict` (with and without the API key where relevant) and print a pass/fail summary. A single manual spot-check, if you want one:

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

### Run tests

```bash
pytest
```

```bash
python -m pytest tests/test_sql_views.py
```

or to run the full test suite:

```bash
python -m pytest
```

## Power BI Dashboard Setup

This section documents how to set up, open, and refresh `dashboard/churn_dashboard.pbix` locally.

### Prerequisites

Before opening the dashboard, the database must be initialized and populated:

```bash
python database/init_db.py
python etl/load_to_db.py
python database/init_views.py
```

Confirm the ETL completed successfully — you should see all rows from the raw dataset (7,043 for the current dataset) inserted into `database/churn.db`.

### 1. Install a SQLite ODBC driver

Install the **SQLite3 ODBC Driver (64-bit)** on your machine. This is the driver version validated against this dashboard:

- Driver: SQLite3 ODBC Driver
- Version: 1.34455.00.00 (64-bit)

Installation source and steps will depend on your OS — search for "SQLite ODBC Driver 64-bit" from a trusted driver provider (e.g. ch-werner.de/sqliteodbc) and follow the installer for your platform.

### 2. Configure an ODBC DSN

Create a **System DSN** pointing at your local `database/churn.db` file. Name the DSN `ChurnDB` (the dashboard's data source expects this name).

Steps (Windows):
1. Open **ODBC Data Sources (64-bit)** from Windows search.
2. Go to the **System DSN** tab → **Add**.
3. Select the SQLite3 ODBC Driver.
4. Set the DSN name to `ChurnDB` and point the database path at your local `database/churn.db`.
5. Save.

> Do not commit your local DSN configuration or any absolute file paths — these are machine-specific and are already excluded via `.gitignore`.

### 3. Set the ProjectPath parameter

The Model Predictions page reads `evaluation/model_comparison.csv` via a Power Query parameter called `ProjectPath`, so each person needs to point it at their own local copy of the repo before refreshing:

1. Open `dashboard/churn_dashboard.pbix` in Power BI Desktop.
2. Go to **Transform Data → Edit Parameters**.
3. Set `ProjectPath` to the full local path of your cloned repo folder. **Do not end the path with a trailing `/` or `\`.**
4. Click **OK**, then refresh (see step 5 below).

This is a one-time local setup step, same as the DSN above — it is not committed with any specific person's path baked in.

### 4. Connect Power BI to the DSN

1. If prompted for a data source, go to **Get Data → ODBC** and select the `ChurnDB` DSN.
2. Confirm the following objects are visible and queryable:
   - `customers`
   - `view_churn_by_contract`
   - `view_churn_by_tenure_bucket`
3. If visuals appear empty after connecting, use **Refresh** (Home tab → Refresh) to force Power BI to re-query the live ODBC connection.

### 5. Refreshing the dashboard

Whenever the underlying data changes (new ETL run, updated views, or a new model evaluation in `evaluation/model_comparison.md`):

1. Re-run the relevant pipeline step (ETL, views, or model evaluation/CSV regeneration — see `evaluation/generate_model_comparison_csv.py`).
2. Open `dashboard/churn_dashboard.pbix` in Power BI Desktop.
3. Click **Refresh** on the Home tab to pull the latest data through the live ODBC connection.
4. Save the file.

No credentials or machine-specific paths (e.g. absolute local file paths, usernames) should ever be committed alongside the `.pbix` file. The DSN name (`ChurnDB`) and the `ProjectPath` parameter are the only environment-specific details the dashboard depends on, and both must be set locally by each team member following the steps above.

---

## Stretch Goals

If core milestones (M0–M6) finish ahead of schedule, the following are owned by Michael and pursued at his discretion:

- SHAP explainability
- Docker
- GitHub Actions CI
- Deployment to cloud
- PostgreSQL instead of SQLite
- Streamlit demo app

---

## Coding Standards

- **Typing required** on all functions — use the `typing` module or built-in generics.
- **No `print()`** — use the `logging` module for all runtime output.
- **Tests required** for every feature — no hard coverage percentage target, but meaningful tests must exist and CI must pass.
- Pragmatic code is preferred over strict SOLID/clean-architecture adherence — clarity and correctness first.

## Data Dictionary and SQL Views

The project includes supporting documentation and reusable SQL views to simplify business analysis and dashboard development.

### Data Dictionary

The data dictionary documents the customer dataset, including each field's business meaning, example values, and intended use in analytics.

Location:

```
docs/data_dictionary.md
```

> **Note**
>
> The data dictionary reflects the current SQLite schema (customers table) and should be updated if the schema changes in future revisions.

### SQL Views

The following reusable SQL views are available.

| View | Description |
|------|-------------|
| view_churn_by_contract | Churn metrics grouped by contract type |
| view_churn_by_tenure_bucket | Churn metrics grouped by customer tenure |

These views are designed for downstream reporting and Power BI dashboards.

These views are created by running:

```bash
python database/init_views.py
```

They are intended for reuse in Power BI dashboards and SQL analytics.