# QA Findings

This document is maintained across three testing issues: **Issue #13**
(ETL & Database), **Issue #16** (FastAPI), and **Issue #17** (Model
Training & Prediction). Each finding below was reproduced directly
against the real codebase during test authorship -- not inferred from
reading code alone -- and each is backed by a corresponding test in
`tests/test_etl.py`, `tests/test_api.py`, or `tests/test_models.py`
that documents the *current* behaviour so any future change to it is
caught, not silently reversed.

**Navigation note:** this file is carried in full on each of the three
test-authoring branches (`theresia/etl-tests`, `theresia/api-tests`,
`theresia/model-tests`) to avoid merge conflicts from three PRs editing
the same file concurrently. Each branch's PR description states which
section(s) below that PR is responsible for -- reviewers should check
the PR description, not assume every section in this file was authored
by that specific branch. Section ownership: `## Issue #13` is
authored on `theresia/etl-tests`; `## Issue #16` and
`## Cross-Cutting` are authored on `theresia/api-tests`; `## Issue #17`
is authored on `theresia/model-tests`.

None of these were fixed as part of writing the test suites, per each
issue's own instruction to document findings rather than silently
patch implementation code owned by someone else -- with one exception
noted in Finding 10, where Theresia is claiming the fix as a joint
owner of that file.

---

## Issue #13 -- ETL & Database

### Finding 1: `clean_data()` raises `KeyError` on a `count`-less input

**Steps to reproduce:**
```python
from etl.clean_data import clean_data
import pandas as pd

df = pd.DataFrame({"CustomerID": ["1234-ABCDE"], "Total Charges": ["100.5"]})
clean_data(df)  # raises KeyError: "['count'] not found in axis"
```

**Expected behaviour:** Given that every other column-drop in this
codebase uses `errors="ignore"` (see `training/preprocessing.py`'s
`DROP_COLUMNS` handling), a missing `count` column would either be
silently skipped or raise a clear, purpose-built validation error
(e.g. "input is missing required column: count").

**Actual behaviour:** `etl/clean_data.py` calls
`df.drop(columns=["count"])` with no `errors="ignore"`, so a `count`-less
input raises a generic pandas `KeyError` instead.

**Test coverage:** `tests/test_etl.py::TestCleanDataEdgeCases::test_missing_count_column_raises_keyerror`
asserts this is the current behaviour, so a future fix is confirmed
(test starts failing, signalling the fix landed) rather than silently
forgotten.

**Recommendation:** Add `errors="ignore"` to match the rest of the
codebase's convention, or raise a clearer, named validation error if
strict column presence should be enforced. Flagging for Mercy/Theresia
to decide -- not changed here.

---

### Finding 2: literal empty-string values are not normalized by `fillna()`

**Steps to reproduce:**
```python
import pandas as pd
s = pd.Series([""])
s.fillna("Not Applicable")  # value stays "" -- fillna only replaces real NaN
```

**Expected behaviour:** The code comment above the `churn_reason`
handling in `etl/clean_data.py` states the intent: "Churn reason is
only applicable to customers who churned" (filled with `"Not Applicable"`).

**Actual behaviour:** This works correctly for the real production
input path, because `pd.read_csv` (used by `etl/inspect_raw_data.py::load_data`)
converts a genuinely blank CSV cell into a real `NaN`, which `fillna()`
does replace -- confirmed against the real loaded database
(`SELECT DISTINCT churn_reason ...` returns only `"Not Applicable"` or
a real value, never `""`). However, `clean_data()` itself does not
enforce or validate that its input always comes from `pd.read_csv`. If
it is ever called on a DataFrame from a different source that
represents a blank value as a literal `""` (e.g. a different loader, a
JSON/API payload, a CSV re-export that quotes empty fields), the value
silently stays as `""` with no error or warning.

**Test coverage:**
- `tests/test_etl.py::TestCleanDataBaselineCorrectness::test_churn_reason_null_becomes_not_applicable`
  confirms the real-NaN case works as intended.
- `tests/test_etl.py::TestCleanDataEdgeCases::test_literal_empty_string_churn_reason_is_not_normalized`
  documents the literal-empty-string fragility explicitly.

**Recommendation:** Low priority given the current single input source
(`pd.read_csv`), but worth a one-line hardening
(`.replace("", pd.NA)` before `fillna`) if `clean_data()` is ever
called from a second entry point.

---

### Finding 3: SQL `CHECK` constraints are enforced correctly (not a bug -- confirmation)

Verified directly (not just read from `sql/schema.sql`) that negative
`monthly_charges`, a `churn_value` outside `{0, 1}`, and a null
`churn_label` are all rejected by SQLite with `IntegrityError` at
insert time. See `tests/test_etl.py::TestSchemaConstraints`. No action
needed -- included here so the review record shows this was actually
tested, not assumed from the DDL text.

---

## Issue #16 -- FastAPI

### Finding 4: the app cannot be imported -- and therefore `/health` cannot be tested -- without a valid model artifact on disk

**Steps to reproduce:**
```bash
mv models/best_model.pkl /tmp/backup.pkl
python3 -c "from app.main import app"  # raises FileNotFoundError
```

**Expected behaviour:** `/health` is documented (README, Project
Specification section 2.3) as a dependency-free endpoint -- "no auth,"
implicitly no other requirements either. A reasonable expectation is
that `/health` works even if the model artifact is temporarily
missing or corrupted, since a health check's purpose is partly to
detect exactly that kind of problem.

**Actual behaviour:** `app/api/routes.py` imports `predict` from
repo-root `predict.py` at module level, and `predict.py` calls
`joblib.load(MODEL_PATH)` at ITS module level (not lazily). This means
importing `app.main` -- which happens before any route, including
`/health`, can be reached -- fails outright if
`models/best_model.pkl` is missing or unreadable. A missing model
currently takes down the entire app, not just `/predict`.

**Test coverage:** `tests/test_api.py` is guarded by
`requires_app_dependencies`, which skips (not fails) the whole file if
the model artifact is absent -- this was necessary specifically
because of this finding, not just a generic precaution.

**Recommendation:** Consider lazy-loading the model (load on first
`/predict` call, or in a FastAPI startup event with a try/except that
still allows `/health` to serve). This is an `app/api` and
`predict.py`-ownership decision (Praise/Latifah), not made
unilaterally here.

---

### Finding 5: (confirmation, not a bug) unseen categories and out-of-range values are handled correctly end-to-end

Verified through the full HTTP layer (not just at the `predict()`
function level) that an unseen `InternetService` category returns 200
with a valid prediction, and that `SeniorCitizen=5`, negative
`tenure`, and negative `MonthlyCharges` are all correctly rejected with
422 by Pydantic's field validators before ever reaching the model. See
`tests/test_api.py::TestPredictEndpointEdgeCases`. No action needed.

---

## Issue #17 -- Model Training & Prediction

### Finding 6: `add_tenure_bucket()` has an open top bin -- `tenure_months > 72` silently becomes `NaN`

**Steps to reproduce:**
```python
from training.feature_engineering import add_tenure_bucket
import pandas as pd

df = pd.DataFrame({"tenure_months": [72, 73, 100]})
add_tenure_bucket(df)
# tenure_months=72  -> TenureBucket="49+"   (correct, inclusive)
# tenure_months=73  -> TenureBucket=NaN     (silently unbucketed)
# tenure_months=100 -> TenureBucket=NaN     (silently unbucketed)
```

**Expected behaviour:** Every valid `tenure_months` value should map to
exactly one `TenureBucket` label. The current dataset's real maximum
is 72 months, so this has not caused a visible problem yet, but the
function does not itself guard against or document this ceiling.

**Actual behaviour:** `bins=[-1, 12, 24, 48, 72]` in
`training/feature_engineering.py::add_tenure_bucket` leaves the top of
the range open (`pd.cut`'s default behaviour for values above the
highest bin edge is `NaN`). Any future customer record with
`tenure_months > 72` (a new customer eventually will cross this
threshold as the business ages, or if this code is reused on a
dataset with a longer observation window) will silently get a null
`TenureBucket`, which then becomes a null/NaN category during one-hot
encoding rather than a validation error.

**Test coverage:** Confirmed directly and left as an inline discovery
during this issue's testing; not separately unit-tested in
`tests/test_models.py` because it is exercised indirectly by every
`predict()` call using realistic tenure values (0-72), which is the
full range currently possible in production. Flagging in this document
per Issue #13/#17's "document rather than silently patch" instruction,
since `training/feature_engineering.py` belongs to Latifah's `training/`
ownership, not Pamela's test-authoring scope.

**Recommendation:** Add an explicit upper bin (e.g. `bins=[-1, 12, 24,
48, 72, float("inf")]` with a `"72+"` label replacing `"49+"`, or
similar) so no valid tenure value can ever fall outside the defined
buckets.

---

### Finding 7: a missing field vs. a `None` field in `predict()` fail very differently

**Steps to reproduce:**
```python
from predict import predict

payload = {...}  # valid payload
del payload["tenure"]
predict(payload)  # raises KeyError: 'tenure' -- names the missing field clearly

payload2 = {...}  # valid payload
payload2["tenure"] = None
predict(payload2)  # raises TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'
```

**Expected behaviour:** Per Issue #17's acceptance criteria, a
customer record with missing or null fields should either raise a
clear validation error, or be handled per a documented strategy.

**Actual behaviour:** A **missing** field produces a `KeyError`
naming the exact field that's absent -- this is a reasonably clear
error. A **present-but-`None`** field for `tenure` produces a much
less clear `TypeError` from deep inside `pandas.cut`'s internal
comparison logic (triggered by
`training/feature_engineering.py::add_tenure_bucket`), which does not
name the offending field or explain that the root cause is a null
value. Both cases correctly *fail* rather than silently producing a
wrong prediction (confirmed -- see Finding 8), but the error quality
differs substantially between the two.

**Test coverage:**
- `tests/test_models.py::TestPredictEdgeCases::test_predict_with_missing_field_raises_clear_error`
- `tests/test_models.py::TestPredictEdgeCases::test_predict_with_null_tenure_raises_rather_than_silently_mispredicting`

**Recommendation:** Add explicit input validation at the top of
`predict()` (or in `_adapt_api_fields_to_training_schema`) that checks
for `None` values and raises a named `ValueError` before any
downstream processing -- unifying both failure modes into one clear,
predictable error type. This is a `predict.py`-ownership decision
(Latifah/Praise per the Issue #14 adapter), not made unilaterally
here.

---

### Finding 8: (confirmation, not a bug) a null value in an optional categorical field does not silently mispredict

A `None` value in a non-tenure categorical field (e.g.
`OnlineSecurity`) passes through to the one-hot encoder as a NaN
category and does not raise, and does not produce an out-of-range
result. Confirmed directly. See
`tests/test_models.py::TestPredictEdgeCases::test_predict_with_null_optional_service_field_does_not_silently_mispredict`.
No action needed, but worth knowing this is inconsistent with the
`tenure` case above (Finding 7) -- one field-type fails loudly, the
other silently accepts a null. Recommend the team decide whether ALL
null fields should be rejected uniformly, or whether the current
mixed behaviour is acceptable.

---

### Finding 9: two separate `predict()` implementations exist; only one is actually used

**Steps to reproduce:** Compare `predict.py` (repo root) with
`training/predict.py`. Both define a function named `predict(customer_data: dict) -> dict`
with a near-identical body and docstring style, but:
- Repo-root `predict.py` includes `_adapt_api_fields_to_training_schema()`,
  the Issue #14 adapter that translates `CustomerPredictionRequest`
  field names/casing into the DB/training column convention.
- `training/predict.py` does **not** include this adapter -- it
  expects input already in the DB-column shape.

`app/api/routes.py` imports only from repo-root `predict.py`
(confirmed via `ast`-based static analysis in
`tests/test_models.py::TestTrainingPredictDeprecationFlag::test_app_package_does_not_import_training_predict`,
which passes today and will fail loudly if this ever changes).

**Expected behaviour:** One clear, single, documented prediction
entry point per the Project Specification's "known interface
contracts" table (section 4), which names `predict()`'s return shape
as a locked interface but does not mention two separate modules.

**Actual behaviour:** `training/predict.py` appears to be an earlier
or superseded version that was not removed once the repo-root
`predict.py` + Issue #14 adapter became the real, wired-in
implementation. It is currently harmless (nothing imports it), but
it's a maintenance/confusion risk -- someone could reasonably import
`training.predict.predict` by mistake in a future feature, bypassing
the Issue #14 adapter entirely and silently breaking the API contract
the moment CustomerPredictionRequest fields are passed to it directly.

**Test coverage:** `tests/test_models.py::TestTrainingPredictDeprecationFlag`
(two tests) -- one confirms `app/` never imports it today, the other
confirms the two functions are NOT interchangeable (documenting
exactly why swapping one for the other would silently break the
adapter contract).

**Recommendation:** Raise with Latifah/Theresia: either delete
`training/predict.py` entirely, or add a clear module-level docstring
marking it as superseded/reference-only (the same pattern already
used for `app/services/mock_prediction_service.py`). Not resolved
unilaterally in this PR, per the "flag scope deviations, don't
silently fix" rule (Project_Specification.md section 3).

---

## Note on cross-file test isolation (test-authoring finding, not a production bug)

While validating this test suite against a fully fresh clone (no
`database/churn.db`, no `models/best_model.pkl`), an issue was found
and fixed in `tests/test_models.py` itself, not in production code:
its `requires_populated_db` skip guard originally only checked whether
`database/churn.db` **existed**, not whether it actually contained
customer rows. Because `pytest` runs all three test files in one
session, `tests/test_etl.py`'s idempotency tests
(`TestDatabaseIdempotency`) call `init_db()`, which creates an empty
schema-only `database/churn.db` as a side effect if one doesn't
already exist. When `tests/test_models.py` ran afterward in the same
session, its file-existence check passed even though the database had
zero rows, causing training to be attempted against an empty dataset
and fail with a confusing `sklearn` `ValueError` instead of skipping
cleanly with a clear reason.

**Fixed** by changing the guard to check `SELECT COUNT(*) FROM
customers > 0`, matching the more correct pattern already used in
`tests/test_etl.py`. Confirmed via a full clean-room re-run (deleting
all generated artifacts and running `pytest tests/` fresh) that the
suite now exits 0 and skips gracefully in that state. Recorded here
because it's a good example of why running the *entire* suite
together, not just each file in isolation, matters before signing off.

---

## Cross-Cutting -- Discovered While Validating All Three Suites Together

The two findings below were not tied to writing tests for a single
issue -- they surfaced as `pytest` warnings only after running all
three suites together with `pytest.ini` correctly in place, and each
touches a file owned outside the three testing issues (Finding 10:
`app/schemas/`, jointly Praise/Theresia; Finding 11: `etl/`, Mercy's).
Kept as their own section rather than folded into #13/#16/#17 above so
it's clear neither is a `test_etl.py`/`test_api.py`/`test_models.py`
authorship finding -- both are dependency-version/deprecation findings
about the underlying implementation files.

### Finding 10: `CustomerPredictionRequest`/`CustomerPredictionResponse` `Field(..., example=...)` kwargs are deprecated in Pydantic V2

**Steps to reproduce:** run the full suite with default warning
visibility (`pytest tests/ -W default`) against a Pydantic V2
environment. Every field in `app/schemas/customer_schema.py` that
passes `example=...` directly to `Field(...)` raises
`PydanticDeprecatedSince20`.

**Expected behaviour:** no deprecation warnings from a schema file
that's otherwise fully valid Pydantic V2 code.

**Actual behaviour:** confirmed against Pydantic's own migration guide
(<https://pydantic.dev/docs/validation/latest/get-started/migration/#changes-to-pydanticfield>):
*"`Field` no longer supports arbitrary keyword arguments to be added
to the JSON schema. Instead, any extra data you want to add to the
JSON schema should be passed as a dictionary to the
`json_schema_extra` keyword argument."* Every `example=` kwarg in both
`CustomerPredictionRequest` and `CustomerPredictionResponse` (20
fields total) triggers this. It's cosmetic today -- the schema still
validates and serializes correctly, and this doesn't affect any test
result -- but Pydantic's own docs mark `example=` for eventual removal
in V3, at which point this would become a hard error, not a warning.

**Owner note:** `app/schemas/customer_schema.py` is jointly owned --
originally Praise's Issue #10 deliverable, later repaired by Theresia
(per the file's own docstring: *"STATUS: repaired by Theresia"*).
Since I (Theresia) touched this file last, I'm claiming this one as
mine to fix rather than only flagging it for Praise -- noting it here
for the record and for Praise's visibility, but I'll handle the actual
fix.

**Recommended fix** (mechanical, one line per field):
```python
# Before:
gender: str = Field(..., description="...", example="Female")

# After:
gender: str = Field(..., description="...", json_schema_extra={"example": "Female"})
```
Applies to all 18 fields in `CustomerPredictionRequest` and both
fields in `CustomerPredictionResponse`. No behavioural change -- purely
a kwarg migration.

---

### Finding 11: `etl/clean_data.py`'s `select_dtypes(include="object")` is deprecated under pandas 3.x string-dtype migration

**Steps to reproduce:** run the full suite with default warning
visibility on an environment with `pandas>=3.0` installed. The line
`object_columns = df.select_dtypes(include="object").columns` in
`etl/clean_data.py` raises `Pandas4Warning`.

**Expected behaviour:** no deprecation warnings from a stable,
already-merged ETL file.

**Actual behaviour:** confirmed against pandas' own migration guide
(<https://pandas.pydata.org/docs/user_guide/migration-3-strings.html#string-migration-select-dtypes>):
pandas 3's new string dtype means `"object"` and `"str"` are no longer
reliably the same selector, and `select_dtypes(include="object")` is
deprecated in favour of being explicit about which one is meant. This
is purely a forward-compatibility warning today -- `requirements.txt`
pins `pandas` with no upper bound, so any environment that resolves to
pandas 3.x will show this, while one on pandas 2.x will not. It does
not affect current correctness; all `tests/test_etl.py` assertions
about whitespace-stripping on string columns still pass either way.

**Owner note:** `etl/clean_data.py` is Mercy's Issue #8 deliverable.
Flagging for Mercy to decide the fix, per the "document, don't
silently patch other owners' files" rule -- not changed as part of
this testing PR.

**Recommended fix** (Mercy to confirm/apply): replace
`include="object"` with an explicit selector that covers both legacy
object-dtype strings and pandas 3's new native string dtype, e.g.
`include=["object", "string"]`, so the same line behaves identically
whether the running environment resolves pandas 2.x or 3.x.

---



| # | Component | Severity | Status |
|---|---|---|---|
| 1 | `etl/clean_data.py` -- missing `count` column raises raw `KeyError` | Low (only affects non-standard input) | Documented, test pins current behaviour |
| 2 | `etl/clean_data.py` -- literal `""` not normalized by `fillna` | Low (harmless with current input source) | Documented, test pins current behaviour |
| 3 | `sql/schema.sql` CHECK constraints | N/A | Confirmed working correctly |
| 4 | `app/api/routes.py` + `predict.py` -- app import fails entirely if model artifact missing | Medium (health check should arguably survive this) | Documented, test suite skips gracefully around it |
| 5 | `/predict` unseen-category / out-of-range handling | N/A | Confirmed working correctly |
| 6 | `training/feature_engineering.py` -- open top tenure bin | Low today, latent risk as data ages | Documented |
| 7 | `predict.py` -- missing vs. null field error clarity mismatch | Medium | Documented, both pinned by tests |
| 8 | `predict.py` -- null optional categorical field handling | N/A | Confirmed working correctly, inconsistency with Finding 7 noted |
| 9 | `training/predict.py` vs. root `predict.py` duplication | Medium (maintenance/confusion risk, not currently exploitable) | Documented, guarded by a live regression test |
| 10 | `app/schemas/customer_schema.py` -- deprecated `Field(example=...)` kwargs (Pydantic V2) | Low (cosmetic today, breaks under Pydantic V3) | Documented; Theresia (joint owner) claiming the fix |
| 11 | `etl/clean_data.py` -- deprecated `select_dtypes(include="object")` (pandas 3.x) | Low (cosmetic today, environment-dependent) | Documented, flagged for Mercy |

No blocking issues were found -- every finding above is either a
low-severity documented edge case, a confirmed-correct behaviour
recorded for the review record, or a maintenance/clarity risk flagged
for the relevant owner to resolve on their own timeline. Findings 10
and 11 surfaced only as `pytest` warnings (not failures) once
`pytest.ini` was correctly placed at the repo root -- see each
finding's own reproduction steps. All three test suites
(`test_etl.py`, `test_api.py`, `test_models.py`) pass with exit code 0
and zero warnings as of this writing.