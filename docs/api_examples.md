# API Examples

This document provides example requests and responses for the Customer Churn Prediction & BI Platform API.

## Authentication

All endpoints except `/health` require API key authentication.

Include the following header in authenticated requests:

```http
Authorization: Bearer $API_KEY
```

Replace `$API_KEY` with your configured API key.

---

## GET /health

Returns the health status of the API.

### Example Request

```bash
curl http://localhost:8000/health
```

### Example Response

```json
{
  "status": "ok"
}
```

---

## GET /customers

Returns customer records from the SQLite database.

### Example Request

```bash
curl -X GET http://localhost:8000/customers \
  -H "Authorization: Bearer $API_KEY"
```

### Example Response

```json
[
  {
    "customer_id": "7590-VHVEG",
    "gender": "Female",
    "senior_citizen": 0,
    "partner": "Yes",
    "dependents": "No",
    "tenure": 12,
    "monthly_charges": 70.05,
    "total_charges": 840.60,
    "churn_label": "No"
  }
]
```

> **Note:** The endpoint returns customer records retrieved directly from the `customers` table. The example above shows a subset of the available fields for readability.

---

## GET /kpis

Returns executive KPI metrics computed from the current customer data.

### Example Request

```bash
curl -X GET http://localhost:8000/kpis \
  -H "Authorization: Bearer $API_KEY"
```

### Example Response

```json
{
  "customer_count": 7043,
  "overall_churn_rate": 26.54,
  "retention_rate": 73.46,
  "average_monthly_charges": 64.76,
  "total_monthly_revenue": 456116.60
}
```

> **Note:** Values shown above are example outputs. Actual values are calculated from the current SQLite database.

---

## POST /predict

Generates a churn prediction using the trained machine learning model.

### Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.05,
    "TotalCharges": 840.60
  }'
```

### Example Response

```json
{
  "churn_probability": 0.65,
  "churn_prediction": true
}
```

### Possible Error Response

```json
{
  "detail": "Prediction failed. See server logs for details."
}
```

---

## GET /model-metrics

Returns evaluation metrics for the trained machine learning model.

### Example Request

```bash
curl -X GET http://localhost:8000/model-metrics \
  -H "Authorization: Bearer $API_KEY"
```

### Example Response

```json
{
  "accuracy": 0.84,
  "precision": 0.79,
  "recall": 0.73,
  "roc_auc": 0.88
}
```

### Possible Error Response

```json
{
  "detail": "Model metrics are unavailable. Run the training pipeline first."
}
```

---

## Endpoint Summary

| Endpoint | Method | Authentication | Description |
|----------|--------|----------------|-------------|
| `/health` | GET | No | Returns API health status. |
| `/customers` | GET | Yes | Returns customer records from the SQLite database. |
| `/kpis` | GET | Yes | Returns executive KPI metrics computed from customer data. |
| `/predict` | POST | Yes | Predicts customer churn using the trained machine learning model. |
| `/model-metrics` | GET | Yes | Returns evaluation metrics for the trained model. |

## Notes

- All authenticated endpoints require an API key supplied in the `Authorization` header.
- The `/predict` endpoint accepts the `CustomerPredictionRequest` schema defined in `app/schemas/customer_schema.py`.
- The `/predict` endpoint returns the `CustomerPredictionResponse` schema containing:
  - `churn_probability` (float)
  - `churn_prediction` (boolean)
- Example values in this document are for demonstration purposes. Actual values depend on the current database contents and trained machine learning model.