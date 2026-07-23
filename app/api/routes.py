"""
Issue #10 -- FastAPI Scaffold -- app/api/routes.py

All 5 endpoints are implemented. /health and /predict return real
(mocked, for /predict) responses. /customers, /kpis, and
/model-metrics return placeholder data on purpose: Mercy's
CustomerRepository (#8) and Salome's SQL views (#9) are not yet
merged, and the issue explicitly allows a temporary mock matching the
expected interface in that situation. Each placeholder is flagged in
PR #10's Notes section per spec, and each function's docstring/comment
notes what should replace it once the relevant dependency merges.
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends

from app.schemas.customer_schema import CustomerPredictionRequest, CustomerPredictionResponse
from app.services.auth_service import verify_api_key
from app.services.mock_prediction_service import mock_predict

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/customers", dependencies=[Depends(verify_api_key)])
def get_customers() -> list[dict[str, Any]]:
    # PLACEHOLDER (Issue #10): Mercy's CustomerRepository (#8) is not
    # yet merged. The two records below are temporary mock data, in
    # the same shape CustomerRepository.get_all() will return --
    # list[dict[str, Any]] -- so the swap below is a drop-in
    # replacement, not a rewrite. Flagged in PR #10's Notes section.
    #
    # Once #8 merges, replace this whole function body with:
    #     from app.repository.customer_repository import CustomerRepository
    #     return CustomerRepository().get_all()
    logger.info("get_customers called (temporary mock -- Issue #8 not yet merged)")      

    return [
    {
        "customerID": "C001",
        "gender": "Male",
        "tenure": 24,
        "MonthlyCharges": 234.00,
        "Churn": "Yes",
    },
    {
        "customerID": "C002",
        "gender": "Female",
        "tenure": 12,
        "MonthlyCharges": 120.50,
        "Churn": "No",
    },
    ]


@router.get("/kpis", dependencies=[Depends(verify_api_key)])
def get_kpis() -> dict[str, Any]:
    # PLACEHOLDER (Issue #10): Salome's SQL views (#9) are not yet
    # merged, so the KPI values below are temporary mock data rather
    # than a live query. Shape (churn rate, avg monthly charges,
    # customer count, etc.) was chosen to match what Joyce's
    # dashboard work is likely to expect. Flagged in PR #10's Notes
    # section. Once #9 merges, replace this with a query against the
    # relevant view(s) in sql/views.sql.
    logger.info("get_kpis called (temporary mock -- Issue #9 not yet merged)")

    return {
        "customer_count": 7043,
        "overall_churn_rate": 26.5,
        "retention_rate": 73.5,
        "average_monthly_charges": 64.76,
        "total_monthly_revenue": 456321.87,
    }

@router.post("/predict", response_model=CustomerPredictionResponse, dependencies=[Depends(verify_api_key)])
def predict(request: CustomerPredictionRequest) -> CustomerPredictionResponse:
    result = mock_predict(request.model_dump())
    return CustomerPredictionResponse(**result)


@router.get("/model-metrics", dependencies=[Depends(verify_api_key)])
def get_model_metrics() -> dict[str, float]:
    # PLACEHOLDER (Issue #10): fixed placeholder values until
    # Latifah's real evaluation output exists (#11) and is wired in
    # for real (#14). Required keys per the issue spec -- accuracy,
    # precision, recall, roc_auc -- are all present; exact values are
    # not meaningful yet.
    logger.info("get_model_metrics called (placeholder metrics)")
    
    return {
    "accuracy": 0.89,
    "precision": 0.86,
    "recall": 0.81,
    "roc_auc": 0.91,
    }