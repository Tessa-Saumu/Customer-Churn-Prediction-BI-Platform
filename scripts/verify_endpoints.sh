#!/usr/bin/env bash
# Local verification script for Issue #10 (FastAPI Scaffold).
#
# Run this against a locally running instance of the API:
#   1. In one terminal: uvicorn app.main:app --reload
#   2. In another terminal: ./verify_endpoints.sh
#
# Requires .env to be set up (cp .env.example .env, then fill in a real
# API_KEY) and the server to already be running on localhost:8000.

set -u

API_KEY="${API_KEY:-}"
BASE_URL="${BASE_URL:-http://localhost:8000}"

if [ -z "$API_KEY" ]; then
    echo "Set API_KEY before running, matching the value in your .env file."
    echo "Example: API_KEY=local-dev-key-123 ./verify_endpoints.sh"
    exit 1
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

echo "Verifying against $BASE_URL"
echo "----------------------------------------"

check "GET /health (no auth)" 200 \
    "$BASE_URL/health"

check "GET /customers without API key -> 401" 401 \
    "$BASE_URL/customers"

check "GET /customers with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/customers"

check "GET /kpis without API key -> 401" 401 \
    "$BASE_URL/kpis"

check "GET /kpis with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/kpis"

check "GET /model-metrics with API key -> 200" 200 \
    -H "X-API-Key: $API_KEY" "$BASE_URL/model-metrics"

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

echo "----------------------------------------"
echo "Results: $pass passed, $fail failed"

if [ "$fail" -gt 0 ]; then
    exit 1
fi