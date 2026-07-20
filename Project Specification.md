# Project Specification — Customer Churn Prediction & BI Platform

**Purpose of this document:** this is the review reference. When a PR lands, check the actual implementation against the relevant section below — not just against the originating issue's checklist. An issue can be technically "done" while quietly drifting from the contract other people's work depends on; this document is where that contract lives in one place.

This document does not introduce anything new — every item below was already decided during planning and is reflected in the issues and README. This is a reorganization for review purposes, not a new set of requirements.

---

## 1. System Overview

An end-to-end platform: raw CSV → cleaned SQLite database → SQL analysis layer → feature engineering → 5 trained models → FastAPI prediction service → Power BI dashboard.

```
CSV → ETL Pipeline → Clean Database (SQLite)
                           │
                           ├──► SQL Analysis (views + queries)
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

**Dataset:** [IBM Telco Customer Churn — Cognos Analytics version](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset). Note: schema must be derived from the actual downloaded file's columns (this version includes extras like Churn Score, CLTV, Churn Reason beyond the commonly-cited 21-feature dataset) — reject any PR that assumes a schema from general knowledge of "the Telco dataset" rather than from the real inspected file.

---

## 2. Component Contracts

Each section below is what a passing PR for that component must actually satisfy. Use this alongside — not instead of — the specific issue's acceptance criteria.

### 2.1 ETL & Database (Mercy — Issue #8)

**Owns:** `etl/`, `database/`, `app/repository/`, `sql/schema.sql`

**Contract:**
- `data/raw/telco_churn_raw.csv` exists (the real downloaded file, not a synthetic sample).
- `etl/inspect_raw_data.py` runs standalone (`python3 etl/inspect_raw_data.py`) and prints column names, dtypes, null counts, row/column counts. **Must have `if __name__ == "__main__":` guard.**
- `sql/schema.sql` contains valid DDL for at least a `customers` table, derived from the actual inspected columns — not assumed.
- `database/db_connection.py` exposes a typed `get_connection() -> sqlite3.Connection`.
- `database/init_db.py` runs standalone, is idempotent (`CREATE TABLE IF NOT EXISTS` — running twice does not error). **Must have `if __name__ == "__main__":` guard.**
- `etl/clean_data.py` handles missing values with a documented strategy (code comment explaining the choice, not just the code).
- `etl/load_to_db.py` runs standalone, loads cleaned data into the `customers` table. **Must have `if __name__ == "__main__":` guard.**
- `app/repository/customer_repository.py` exposes a typed `CustomerRepository` class with at minimum `get_all() -> list[dict]` and `get_by_id(customer_id: str) -> dict | None`.
- **Reject if:** any downstream code (Praise's API, Salome's SQL) queries the raw CSV or raw SQL directly instead of going through `CustomerRepository` or the finalized schema.
- **Reject if:** `docs/data_dictionary.md` is touched by this PR at all — that file belongs entirely to Salome's Issue #9, not Mercy's Issue #8.

---

### 2.2 SQL Analysis & Data Dictionary (Salome — Issue #9)

**Owns:** `sql/analysis_queries.sql`, `sql/views.sql`, `docs/data_dictionary.md`, `docs/sql_analysis_summary.md`

**Contract:**
- 5 required exploratory queries exist in `sql/analysis_queries.sql`: overall churn rate, churn by contract type, churn by tenure bucket, average monthly charges (churned vs. not), top 3 correlated features. Each has a one-sentence comment stating the business question it answers.
- At least 2 named `CREATE VIEW` statements exist in `sql/views.sql` (e.g. `view_churn_by_contract`, `view_churn_by_tenure_bucket`) — these are what Joyce's Power BI dashboard connects to directly, so names must be stable and clearly documented.
- `docs/data_dictionary.md` is built **entirely by Salome, from scratch** — sourced from Mercy's finalized schema and `inspect_raw_data.py` output, not from a partial version anyone else started. Every column in the final schema has: name, type, example value, business-context description.
- **Reject if:** `docs/data_dictionary.md` shows any contribution from Mercy, Praise, or Latifah in this PR's diff — this is Salome's deliverable exclusively, per the brief.
- **Reject if:** views reference columns or tables that don't match Mercy's actual finalized schema (a sign the PR was built against an assumed or stale schema).
- **Dependency note for reviewers:** the exploratory queries and business-question drafting can legitimately be written before Issue #8 merges (against the raw CSV directly) — only the final views require the merged schema. Don't reject a PR solely for having started before #8 merged; check that the *views specifically* point at real, current tables.

---

### 2.3 FastAPI Scaffold (Praise — Issue #10, then Issue #14 for real integration)

**Owns:** `app/api/`, `app/services/`, `app/schemas/`, `app/main.py`

**Contract (Issue #10 — scaffold stage):**
- All 5 endpoints exist: `GET /health` (no auth), `GET /customers`, `GET /kpis`, `POST /predict`, `GET /model-metrics` (all four require `X-API-Key` header).
- `app/services/auth_service.py` returns HTTP 401 for missing/invalid API key.
- `/predict` uses a clearly-commented mocked prediction function at this stage — real integration is a separate issue (#14), not expected here.
- Request/response schemas in `app/schemas/` match exactly: response for `/predict` contains `churn_probability: float` and `churn_prediction: bool`.
- `.env.example` documents `API_KEY`.
- **Reject if:** any endpoint is missing auth that should have it, or has auth on `/health` that shouldn't.
- **Reject if:** placeholder/hardcoded data used in `/customers` or `/kpis` is NOT flagged explicitly in the PR's "Notes" section — silent placeholders are a real risk here since they're easy to forget once real data is available.

**Contract (Issue #14 — real integration):**
- `mock_prediction_service.py` is removed or explicitly marked as retained-for-reference, not silently left wired into the app.
- `/predict` calls the real `predict()` from repo-root `predict.py` (Latifah's Issue #11).
- `/model-metrics` reads real values from Latifah's evaluation output, not placeholders.
- `/customers` and `/kpis` are confirmed reading from real repository/view data, not any placeholder carried over from Issue #10.
- The public API contract (schema shapes, routes, auth) is unchanged from Issue #10 — only internals should differ.
- **Reject if:** the response schema shape changed as part of this "integration" PR — that's scope creep into a PR that should only be swapping internals.

---

### 2.4 Model Training & Evaluation (Latifah — Issue #11)

**Owns:** `training/`, `evaluation/`, `models/`, `predict.py`

**Contract:**
- Reads data via `CustomerRepository`, not the raw CSV directly.
- All 5 required models trained: **Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM.** No fewer, no substitutions without a flagged deviation.
- All 5 metrics computed per model: Accuracy, Precision, Recall, ROC AUC, Confusion Matrix.
- A clear, stated best-model selection with justification — not just a table with no conclusion.
- `predict.py`'s `predict(customer_data: dict) -> dict` returns exactly `{"churn_probability": float, "churn_prediction": bool}` — this exact shape is load-bearing, since Praise's Issue #14 depends on it without modification.
- **Reject if:** the returned dict shape from `predict()` differs from the above — this breaks Issue #14's integration contract silently.
- **Reject if:** fewer than 5 models are actually trained and evaluated, even if the code "works" for the ones that are there.

---

### 2.5 Power BI Dashboard (Joyce — Issue #12)

**Owns:** `dashboard/`

**Contract:**
- Connects via ODBC to `database/churn.db` — not a static export, not a manually-entered dataset standing in for a live connection.
- All 5 required pages exist and render real data: Executive Overview, Customer Demographics, Churn Drivers, Revenue Impact, Model Predictions.
- Every visual is backed by a live query against Salome's views or the `customers` table — no hardcoded numbers standing in for real data anywhere on any page.
- `dashboard/business_report.md` contains at least 3 distinct, specific recommendations tied to visible dashboard findings — not generic churn-reduction advice unconnected to this project's actual data.
- **Reject if:** any page shows placeholder/sample data rather than a live connection — this is the single most important thing to check, since a dashboard can look complete while quietly not being wired to anything real.

---

### 2.6 Testing (Pamela — Issues #13, #16, #17, #19)

**Owns:** `tests/test_etl.py`, `tests/test_api.py`, `tests/test_models.py`

**Contract:**
- All three test files are authored entirely by Pamela, from scratch — not expanded from a version someone else started. **Reject if `test_etl.py`, `test_api.py`, or `test_models.py` shows authorship/content from Mercy, Praise, or Latifah** — per the brief, these three filenames are Pamela's deliverables exclusively.
- Each file covers both baseline correctness and genuine edge cases (missing data, malformed input, unseen categories), not just happy-path checks.
- `pytest` exits with code 0 for the relevant file(s) in each PR.
- Logging gaps found in other people's code are documented in the PR's "Notes" section for that person to fix — not silently patched by Pamela.
- **Reject if:** a test file only tests the happy path with no edge cases, since the issues explicitly required both.

---

## 3. Cross-Cutting Standards (apply to every PR, regardless of component)

- **Typing:** every function has type hints. No exceptions.
- **No `print()`:** `logging` module only.
- **PR description:** uses the full template from the README, every section filled in (not left as empty headers).
- **Scope deviations:** anything that differs from the originating issue — renamed function, different library, extra feature — is explicitly flagged under "Notes," not silently shipped.
- **No direct pushes to `main`:** every change via Issue → Branch → PR → Theresia's review → Michael's sign-off → Merge.
- **Ownership boundaries are exact, not approximate:** if a brief-listed deliverable (data dictionary, the three named test files) shows contribution from someone other than its named owner, that's a reject-and-request-changes situation regardless of code quality — this preserves the mentorship structure's intent, not just the code's correctness.

---

## 4. Known Interface Contracts (the things that must not silently change)

These are the exact shapes/names that multiple people's work depends on. If a PR changes any of these, it needs explicit cross-team confirmation, not just a "Notes" flag — treat as a stop-and-check, not a proceed-with-caution.

| Interface | Defined by | Depended on by |
|---|---|---|
| `CustomerRepository.get_all()`, `.get_by_id()` return shapes | Mercy (#8) | Praise (#10, #14), Latifah (#11) |
| SQL view names in `sql/views.sql` | Salome (#9) | Joyce (#12) |
| `predict()` return shape (`churn_probability`, `churn_prediction`) | Latifah (#11) | Praise (#14) |
| `/predict`, `/model-metrics` response schemas | Praise (#10) | Joyce (#12, "Model Predictions" page references these) |
| Final database schema / column names | Mercy (#8) | Salome (#9), Latifah (#11), Joyce (#12) |

If any of these change mid-sprint, flag it to every downstream owner directly — this table is exactly where "Joyce and Salome must stay in sync" (already noted in the README) generalizes to the whole team, not just that one pair.
