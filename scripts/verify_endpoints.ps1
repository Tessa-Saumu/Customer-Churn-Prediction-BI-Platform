# Local verification script for Issue #14 (Real Integration).
#
# Superset of Issue #10's verify_endpoints.ps1: keeps every original
# status-code check (auth still behaves the same -- part of Issue
# #14's "no public contract changes" requirement), and adds checks
# that RESPONSE CONTENT is real, not the old mocked/placeholder
# values. A 200 status code alone doesn't prove the mock is gone --
# the old mock also returned 200.
#
# Run this against a locally running instance of the API:
#   1. Run the full pipeline first (see README "Before running the
#      API" section added in Issue #14):
#        python database/init_db.py
#        python etl/load_to_db.py
#        python database/init_views.py
#        python training/evaluate_models.py
#   2. In one terminal:
#        uvicorn app.main:app --reload
#   3. In another terminal:
#        .\verify_endpoints.ps1
#
# Requires a .env file to be set up with a valid API_KEY.
# If the API_KEY environment variable is not already set, this script
# defaults to "local-dev-key-123". Update the default below or set the
# environment variable before running if your application uses a different key.
#
# Optional environment variables:
#   API_KEY   - API key to send in the X-API-Key header.
#   BASE_URL  - Base URL of the running API (default: http://localhost:8000).
#
# This script verifies:
#   - GET  /health                 -> 200 (no authentication)
#   - GET  /customers              -> 401 without API key
#   - GET  /customers              -> 200 with API key, real schema fields
#   - GET  /kpis                   -> 401 without API key
#   - GET  /kpis                   -> 200 with API key, internally consistent
#   - GET  /model-metrics          -> 200 with API key, matches real LightGBM results
#   - POST /predict                -> 401 without API key
#   - POST /predict                -> 200 with API key, real model output (not fixed 0.42)
#   - POST /predict                -> 422 on malformed input
#
# Exit code:
#   0 = All endpoint checks passed.
#   1 = One or more endpoint checks failed.

$API_KEY = if ($env:API_KEY) { $env:API_KEY } else { "local-dev-key-123" }
$BASE_URL = if ($env:BASE_URL) { $env:BASE_URL } else { "http://localhost:8000" }

$headers = @{
    "X-API-Key" = $API_KEY
}

$pass = 0
$fail = 0

function Check-Endpoint {
    param(
        [string]$Description,
        [string]$Method = "GET",
        [string]$Uri,
        [int]$ExpectedStatus,
        [hashtable]$Headers = $null,
        [string]$Body = $null
    )

    # $script:lastResponseContent holds the parsed body of the most
    # recent successful (2xx) call, for Check-Content to inspect.
    $script:lastResponseContent = $null

    try {
        if ($Body) {
            $response = Invoke-WebRequest `
                -Uri $Uri `
                -Method $Method `
                -Headers $Headers `
                -ContentType "application/json" `
                -Body $Body

        }
        else {
            $response = Invoke-WebRequest `
                -Uri $Uri `
                -Method $Method `
                -Headers $Headers
        }

        $status = 200
        $script:lastResponseContent = $response.Content | ConvertFrom-Json
    }
    catch {
        if ($_.Exception.Response) {
            $status = [int]$_.Exception.Response.StatusCode
        }
        else {
            Write-Host "FAIL [No Response] $Description"
            $script:fail++
            return
        }
    }

    if ($status -eq $ExpectedStatus) {
        Write-Host "PASS [$status] $Description" -ForegroundColor Green
        $script:pass++
    }
    else {
        Write-Host "FAIL [$status expected $ExpectedStatus] $Description" -ForegroundColor Red
        $script:fail++
    }
}

# Evaluates a scriptblock against $script:lastResponseContent (set by
# the most recent Check-Endpoint call). Only meaningful immediately
# after a Check-Endpoint call that hit the same endpoint and returned
# 2xx -- if that call failed, $lastResponseContent is $null and this
# check reports FAIL rather than silently passing.
function Check-Content {
    param(
        [string]$Description,
        [scriptblock]$Condition
    )

    if ($null -eq $script:lastResponseContent) {
        Write-Host "FAIL [content, no response body] $Description" -ForegroundColor Red
        $script:fail++
        return
    }

    $result = & $Condition $script:lastResponseContent

    if ($result) {
        Write-Host "PASS [content] $Description" -ForegroundColor Green
        $script:pass++
    }
    else {
        Write-Host "FAIL [content] $Description" -ForegroundColor Red
        Write-Host "      Body: $($script:lastResponseContent | ConvertTo-Json -Compress)"
        $script:fail++
    }
}

Write-Host "Verifying against $BASE_URL"
Write-Host "----------------------------------------"

Check-Endpoint `
    -Description "GET /health" `
    -Uri "$BASE_URL/health" `
    -ExpectedStatus 200

Check-Endpoint `
    -Description "GET /customers without API key" `
    -Uri "$BASE_URL/customers" `
    -ExpectedStatus 401

Check-Endpoint `
    -Description "GET /customers with API key" `
    -Uri "$BASE_URL/customers" `
    -Headers $headers `
    -ExpectedStatus 200

# Issue #14: /customers must be real CustomerRepository data, not
# Issue #10's two hardcoded records (customerID "C001"/"C002" with
# camelCase field names). Real schema uses snake_case customer_id.
Check-Content `
    -Description "GET /customers returns real schema field names (not mock's camelCase)" `
    -Condition { param($c) ($null -ne $c[0].customer_id) -and ($null -eq $c[0].customerID) }

Check-Content `
    -Description "GET /customers row count is not the Issue #10 mock's fixed 2 records" `
    -Condition { param($c) $c.Count -ne 2 }

Check-Endpoint `
    -Description "GET /kpis without API key" `
    -Uri "$BASE_URL/kpis" `
    -ExpectedStatus 401

Check-Endpoint `
    -Description "GET /kpis with API key" `
    -Uri "$BASE_URL/kpis" `
    -Headers $headers `
    -ExpectedStatus 200

# Issue #14: /kpis must be computed from real data. Your real database
# also happens to load 7043 rows (per your ETL run), so that specific
# number is checked directly below AND we check internal consistency,
# which the old fixed mock dict never had to satisfy by construction.
Check-Content `
    -Description "GET /kpis: overall_churn_rate + retention_rate ~= 100" `
    -Condition { param($k) [math]::Abs(($k.overall_churn_rate + $k.retention_rate) - 100) -lt 0.1 }

Check-Content `
    -Description "GET /kpis: customer_count matches real row count (7043 per your ETL run)" `
    -Condition { param($k) $k.customer_count -eq 7043 }

Check-Endpoint `
    -Description "GET /model-metrics with API key" `
    -Uri "$BASE_URL/model-metrics" `
    -Headers $headers `
    -ExpectedStatus 200

# Issue #14: /model-metrics must be real values parsed from
# evaluation/model_comparison.md's Selected Model (LightGBM) block,
# not Issue #10's fixed placeholder {0.89, 0.86, 0.81, 0.91}.
Check-Content `
    -Description "GET /model-metrics does not match the Issue #10 placeholder values" `
    -Condition {
        param($m)
        -not (
            ($m.accuracy -eq 0.89) -and
            ($m.precision -eq 0.86) -and
            ($m.recall -eq 0.81) -and
            ($m.roc_auc -eq 0.91)
        )
    }

Check-Content `
    -Description "GET /model-metrics accuracy matches real Logistic Regression result (~0.8020)" `
    -Condition { param($m) ($m.accuracy -gt 0.801) -and ($m.accuracy -lt 0.803) }

Check-Content `
    -Description "GET /model-metrics roc_auc matches real Logistic Regression result (~0.8494)" `
    -Condition { param($m) ($m.roc_auc -gt 0.849) -and ($m.roc_auc -lt 0.850) }

Check-Endpoint `
    -Description "POST /predict without API key" `
    -Method POST `
    -Uri "$BASE_URL/predict" `
    -Body (@{} | ConvertTo-Json) `
    -ExpectedStatus 401

$body = @{
    gender = "Female"
    SeniorCitizen = 0
    Partner = "Yes"
    Dependents = "No"
    tenure = 12
    PhoneService = "Yes"
    MultipleLines = "No"
    InternetService = "Fiber optic"
    OnlineSecurity = "No"
    OnlineBackup = "Yes"
    DeviceProtection = "No"
    TechSupport = "No"
    StreamingTV = "Yes"
    StreamingMovies = "No"
    Contract = "Month-to-month"
    PaperlessBilling = "Yes"
    PaymentMethod = "Electronic check"
    MonthlyCharges = 70.05
    TotalCharges = 840.60
} | ConvertTo-Json

Check-Endpoint `
    -Description "POST /predict with API key" `
    -Method POST `
    -Uri "$BASE_URL/predict" `
    -Headers $headers `
    -Body $body `
    -ExpectedStatus 200

# Issue #14: response shape is locked (churn_probability, churn_prediction
# only) -- same check as Issue #10 would have made, re-verified here
# since #14 touches this endpoint's internals.
Check-Content `
    -Description "POST /predict response has exactly the locked two keys" `
    -Condition {
        param($p)
        $keys = $p.PSObject.Properties.Name | Sort-Object
        ($keys -join ",") -eq "churn_prediction,churn_probability"
    }

Check-Content `
    -Description "POST /predict churn_probability is in valid [0,1] range" `
    -Condition { param($p) ($p.churn_probability -ge 0) -and ($p.churn_probability -le 1) }

# Issue #14: the old mock ALWAYS returned exactly 0.42 regardless of
# input. This doesn't prove the model is "correct" -- only that it's
# not the fixed mock constant.
Check-Content `
    -Description "POST /predict churn_probability is not the Issue #10 mock's fixed 0.42" `
    -Condition { param($p) $p.churn_probability -ne 0.42 }

# Malformed-input edge case (mock had no validation-failure path worth
# checking since it never called a real model that could reject
# unseen categories/shapes -- this endpoint's error handling is new
# in Issue #14, see routes.py's try/except around real_predict()).
Check-Endpoint `
    -Description "POST /predict with missing required field" `
    -Method POST `
    -Uri "$BASE_URL/predict" `
    -Headers $headers `
    -Body (@{ gender = "Female" } | ConvertTo-Json) `
    -ExpectedStatus 422

Write-Host "----------------------------------------"
Write-Host "Results: $pass passed, $fail failed"

if ($fail -gt 0) {
    exit 1
}