#!/usr/bin/env bash
# Local verification script for Issue #14 (Real Integration).
#
# Superset of Issue #10's verify_endpoints.sh: keeps every original
# status-code check (auth still behaves the same -- that's part of
# Issue #14's "no public contract changes" requirement), and adds
# checks that the RESPONSE CONTENT is real, not the old mocked/
# placeholder values. A 200 status code alone doesn't prove the mock
# is gone -- the old mock also returned 200.
#
# Run this against a locally running instance of the API:
#   1. Run the full pipeline first (see README "Before running the
#      API" section added in Issue #14):
#        python database/init_db.py
#        python etl/load_to_db.py
#        python database/init_views.py
#        python training/evaluate_models.py
#   2. In one terminal: uvicorn app.main:app --reload
#   3. In another terminal: ./verify_endpoints.sh
#
# Requires .env to be set up (cp .env.example .env, then fill in a real
# API_KEY) and the server to already be running on localhost:8000.
#
# Requires `jq` for the content checks below. If jq isn't installed,
# the status-code checks still run; content checks are skipped with a
# warning rather than failing the whole script on a missing tool.

set -u

API_KEY="${API_KEY:-}"
BASE_URL="${BASE_URL:-http://localhost:8000}"

if [ -z "$API_KEY" ]; then
    echo "Set API_KEY before running, matching the value in your .env file."
    echo "Example: API_KEY=local-dev-key-123 ./verify_endpoints.sh"
    exit 1
fi

HAVE_JQ=1
if ! command -v jq >/dev/null 2>&1; then
    HAVE_JQ=0
    echo "WARNING: jq not found -- content checks (Issue #14) will be skipped."
    echo "         Install jq to verify real vs. mocked response content."
    echo ""
fi

pass=0
fail=0

check() {
    local description="$1"
    local expected_status="$2"
    shift 2
    local response
    response=$(curl -s -o /tmp/verify_body.txt -w "%{http_code}" "$@")

    if [ "$response" = "$expected_status" ]; then
        echo "PASS  [$response]  $description"
        pass=$((pass + 1))
    else
        echo "FAIL  [$response, expected $expected_status]  $description"
        echo "      Body: $(cat /tmp/verify_body.txt)"
        fail=$((fail + 1))
    fi
}

# Like check(), but for asserting something about the response BODY
# rather than just the status code. `condition_desc` is a jq boolean
# expression evaluated against the last response body in
# /tmp/verify_body.txt. Only meaningful after a check() call that hit
# the same endpoint immediately before it (reuses /tmp/verify_body.txt).
check_content() {
    local description="$1"
    local jq_filter="$2"

    if [ "$HAVE_JQ" -eq 0 ]; then
        echo "SKIP  (no jq)  $description"
        return
    fi

    if jq -e "$jq_filter" /tmp/verify_body.txt >/dev/null 2>&1; then
        echo "PASS  [content]  $description"
        pass=$((pass + 1))
    else
        echo "FAIL  [content]  $description"
        echo "      Body: $(cat /tmp/verify_body.txt)"
        fail=$((fail + 1))
    fi
}

echo "Verifying against $BASE_URL"
echo "----------------------------------------"

check "GET /health (no auth)" 200 \
    "$BASE_URL/health"

check "GET /customers without API key -> 401" 401 \
    "$BASE_URL/customers"

check "GET /customers with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/customers"

# Issue #14: /customers must be real CustomerRepository data, not
# Issue #10's two hardcoded records (customerID "C001"/"C002" with
# camelCase field names). Real schema uses snake_case customer_id.
check_content "GET /customers returns real schema field names (not mock's camelCase)" \
    '(.[0] | has("customer_id")) and ((.[0] | has("customerID")) | not)'

check_content "GET /customers row count is not the Issue #10 mock's fixed 2 records" \
    'length != 2'

check "GET /kpis without API key -> 401" 401 \
    "$BASE_URL/kpis"

check "GET /kpis with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/kpis"

# Issue #14: /kpis must be computed from real data. Issue #10's mock
# always returned exactly customer_count: 7043. Your real database
# also happens to load 7043 rows (per the training log), so this
# specific number is no longer a reliable "is it real" signal on its
# own -- instead assert internal consistency, which the fixed mock
# dict never had to satisfy by construction.
check_content "GET /kpis: overall_churn_rate + retention_rate ~= 100" \
    '(.overall_churn_rate + .retention_rate) > 99.9 and (.overall_churn_rate + .retention_rate) < 100.1'

check_content "GET /kpis: customer_count matches real row count (7043 per your ETL run)" \
    '.customer_count == 7043'

check "GET /model-metrics with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/model-metrics"

# Issue #14: /model-metrics must be real values parsed from
# evaluation/model_comparison.md's Selected Model (LightGBM) block,
# not Issue #10's fixed placeholder {0.89, 0.86, 0.81, 0.91}.
check_content "GET /model-metrics does not match the Issue #10 placeholder values" \
    '[.accuracy, .precision, .recall, .roc_auc] != [0.89, 0.86, 0.81, 0.91]'

check_content "GET /model-metrics accuracy matches real LightGBM result (~0.9304)" \
    '(.accuracy > 0.929) and (.accuracy < 0.932)'

check_content "GET /model-metrics roc_auc matches real LightGBM result (~0.9818)" \
    '(.roc_auc > 0.981) and (.roc_auc < 0.983)'

check "POST /predict without API key -> 401" 401 \
    -X POST -H "Content-Type: application/json" \
    -d '{}' \
    "$BASE_URL/predict"

check "POST /predict with API key -> 200" 200 \
    -X POST -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
    -d '{
        "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
        "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
        "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes",
        "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check", "MonthlyCharges": 70.05, "TotalCharges": 840.60
    }' \
    "$BASE_URL/predict"

# Issue #14: response shape is locked (churn_probability, churn_prediction
# only) -- same check as Issue #10 would have made, re-verified here
# since #14 touches this endpoint's internals.
check_content "POST /predict response has exactly the locked two keys" \
    '(keys | sort) == ["churn_prediction", "churn_probability"]'

check_content "POST /predict churn_probability is in valid [0,1] range" \
    '(.churn_probability >= 0) and (.churn_probability <= 1)'

# Issue #14: the old mock ALWAYS returned exactly 0.42 regardless of
# input. This doesn't prove the model is "correct" -- only that it's
# not the fixed mock constant.
check_content "POST /predict churn_probability is not the Issue #10 mock's fixed 0.42" \
    '.churn_probability != 0.42'

# Malformed-input edge case (mock had no validation-failure path worth
# checking since it never called a real model that could reject
# unseen categories/shapes -- this endpoint's error handling is new
# in Issue #14, see routes.py's try/except around real_predict()).
check "POST /predict with missing required field -> 422" 422 \
    -X POST -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
    -d '{"gender": "Female"}' \
    "$BASE_URL/predict"

echo "----------------------------------------"
echo "Results: $pass passed, $fail failed"

if [ "$fail" -gt 0 ]; then
    exit 1
fi