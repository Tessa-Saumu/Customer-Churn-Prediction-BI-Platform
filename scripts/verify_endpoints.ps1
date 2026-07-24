# Local verification script for Issue #10 (FastAPI Scaffold).
#
# Run this against a locally running instance of the API:
#   1. In one terminal:
#        uvicorn app.main:app --reload
#   2. In another terminal:
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
#   - GET  /customers              -> 200 with API key
#   - GET  /kpis                   -> 401 without API key
#   - GET  /kpis                   -> 200 with API key
#   - GET  /model-metrics          -> 200 with API key
#   - POST /predict                -> 200 with API key
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

    try {
        if ($Body) {
            Invoke-WebRequest `
                -Uri $Uri `
                -Method $Method `
                -Headers $Headers `
                -ContentType "application/json" `
                -Body $Body | Out-Null
        }
        else {
            Invoke-WebRequest `
                -Uri $Uri `
                -Method $Method `
                -Headers $Headers | Out-Null
        }

        $status = 200
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

Check-Endpoint `
    -Description "GET /kpis without API key" `
    -Uri "$BASE_URL/kpis" `
    -ExpectedStatus 401

Check-Endpoint `
    -Description "GET /kpis with API key" `
    -Uri "$BASE_URL/kpis" `
    -Headers $headers `
    -ExpectedStatus 200

Check-Endpoint `
    -Description "GET /model-metrics with API key" `
    -Uri "$BASE_URL/model-metrics" `
    -Headers $headers `
    -ExpectedStatus 200

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

Write-Host "----------------------------------------"
Write-Host "Results: $pass passed, $fail failed"

if ($fail -gt 0) {
    exit 1
}
