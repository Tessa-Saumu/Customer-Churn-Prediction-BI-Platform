"""
Issue #10 -- FastAPI Scaffold -- app/api/routes.py

All 5 endpoints are implemented. /health and /predict return real
(mocked, for /predict) responses. /customers and /kpis return
placeholder data by deliberate scope decision, not because #8/#9 are
unmerged -- both merged during this sprint. Per spec section 2.3, the
real swap belongs to Issue #14 (real integration), reviewed as its own
unit rather than folded silently into this PR. See Tessa's review note
on Issue #10 for the explicit call. Each placeholder is flagged in PR
#10's Notes section, and each function's comment notes what should
replace it when #14 happens.
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
    # PLACEHOLDER (Issue #10, kept by deliberate scope decision):
    # CustomerRepository (#8) IS merged as of this comment, but the
    # swap to real data is explicitly Issue #14's job, not folded in
    # here -- see spec section 2.3 and Tessa's Issue #10 review note.
    # Two records below are temporary mock data, same shape
    # CustomerRepository.get_all() returns -- list[dict[str, Any]].
    # Flagged in PR #10's Notes section.
    #
    # Issue #14: replace this whole function body with:
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
    # PLACEHOLDER (Issue #10, kept by deliberate scope decision):
    # Salome's SQL views (#9) ARE merged as of this comment, but the
    # swap to a live query is explicitly Issue #14's job, not folded
    # in here -- see spec section 2.3 and Tessa's Issue #10 review
    # note. Values below are temporary mock data. Shape (churn rate,
    # avg monthly charges, customer count, etc.) was chosen to match
    # what Joyce's dashboard work is likely to expect. Flagged in PR
    # #10's Notes section.
    #
    # Issue #14: replace this with a query against the relevant
    # view(s) in sql/views.sql.
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