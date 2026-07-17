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
- **Python 3.12** — confirm with `python3 --version`
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
python3 --version

# Create and activate a virtual environment
python3 -m venv venv
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

## Sprint Board

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

### Run the ETL pipeline

```bash
python3 database/init_db.py
python3 etl/load_to_db.py
```

### Run the API locally

```bash
uvicorn app.main:app --reload
```

Then verify:

```bash
curl http://localhost:8000/health
# {"status": "ok"}

curl -H "X-API-Key: <your-key-from-.env>" http://localhost:8000/customers
```

### Run tests

```bash
pytest
```

### Connect Power BI to the database

1. Install a SQLite ODBC driver locally.
2. Configure an ODBC DSN pointing at `database/churn.db`.
3. In Power BI Desktop, connect using **Get Data → ODBC** and select the configured DSN.
4. Confirm the tables/views (including Salome's named views in `sql/views.sql`) are visible before building dashboard pages.

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
