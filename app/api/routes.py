"""
Issue #10 -- FastAPI Scaffold -- app/api/routes.py

/health and /predict are complete and working below -- read them, they
show the pattern (the auth dependency, the response model). /customers,
/kpis, and /model-metrics are left as TODOs on purpose: Mercy's
CustomerRepository (#8) and Salome's SQL views (#9) aren't merged yet,
and the issue explicitly allows a temporary mock matching the expected
interface in that situation -- so the decision left for you is what a
reasonable placeholder shape looks like, not whether to have one.

IMPORTANT: per the spec, placeholder data in /customers or /kpis must
be flagged explicitly in your PR's "Notes" section -- a silent
placeholder here is an explicit reject condition, not just a style
nitpick.
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
    # TODO: Mercy's CustomerRepository (#8) isn't merged yet, so this
    # needs a temporary mock matching the expected interface -- a
    # list[dict[str, Any]], same shape CustomerRepository.get_all()
    # will return once it exists. Write a couple of representative
    # placeholder customer records (a dict per customer is enough).
    #
    # Once #8 merges, this whole TODO gets replaced with:
    #     from app.repository.customer_repository import CustomerRepository
    #     return CustomerRepository().get_all()
    #
    # Don't forget: flag this placeholder explicitly in your PR's
    # Notes section before it goes up.
    logger.info("get_customers called (temporary mock -- Issue #8 not yet merged)")
    raise NotImplementedError("TODO: return a temporary mock list of customer dicts")


@router.get("/kpis", dependencies=[Depends(verify_api_key)])
def get_kpis() -> dict[str, Any]:
    # TODO: same situation as /customers -- Salome's SQL views (#9)
    # aren't merged yet. Decide on a reasonable placeholder KPI shape
    # (e.g. overall churn rate, average monthly charges, customer
    # count) -- it doesn't need to be real, it needs to be a shape
    # Joyce's dashboard work could plausibly expect later.
    #
    # Same reminder: flag this placeholder explicitly in your PR's
    # Notes section.
    logger.info("get_kpis called (temporary mock -- Issue #9 not yet merged)")
    raise NotImplementedError("TODO: return a temporary mock KPI dict")


@router.post("/predict", response_model=CustomerPredictionResponse, dependencies=[Depends(verify_api_key)])
def predict(request: CustomerPredictionRequest) -> CustomerPredictionResponse:
    result = mock_predict(request.model_dump())
    return CustomerPredictionResponse(**result)


@router.get("/model-metrics", dependencies=[Depends(verify_api_key)])
def get_model_metrics() -> dict[str, float]:
    # TODO: placeholder metrics until Latifah's real evaluation output
    # exists (#11, then wired for real in #14). Required keys per the
    # issue: accuracy, precision, recall, roc_auc. Pick sensible
    # placeholder values (e.g. all 0.0, or a fixed plausible number) --
    # the exact values genuinely don't matter yet since these are
    # explicitly placeholders, just make sure all four keys are there.
    logger.info("get_model_metrics called (placeholder metrics)")
    raise NotImplementedError("TODO: return placeholder accuracy/precision/recall/roc_auc")