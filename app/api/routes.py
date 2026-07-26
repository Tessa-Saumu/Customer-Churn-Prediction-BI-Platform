"""
Issue #14 -- Real Integration -- app/api/routes.py

Swaps every placeholder from Issue #10's scaffold for real
implementations. Per Issue #14's contract: routes/paths, request
schema, response schema, and auth behavior are UNCHANGED from Issue
#10 -- only internals differ. Diff this file against Issue #10's
version to confirm: no route added/removed/renamed, no
`dependencies=[Depends(verify_api_key)]` added or removed, no schema
field added/removed.

Summary of changes from Issue #10:
- /customers: CustomerRepository().get_all() instead of hardcoded list.
- /kpis: app.services.kpi_service.get_kpis() instead of hardcoded dict.
- /predict: predict.py's real predict() instead of mock_predict().
- /model-metrics: app.services.metrics_service.get_model_metrics()
  instead of hardcoded dict.
- mock_prediction_service import removed entirely (file itself is
  archived, not deleted -- see that file's own docstring).
"""

import logging
import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.repository.customer_repository import CustomerRepository
from app.schemas.customer_schema import CustomerPredictionRequest, CustomerPredictionResponse
from app.services.auth_service import verify_api_key
from app.services.kpi_service import get_kpis as compute_kpis
from app.services.metrics_service import get_model_metrics as load_model_metrics

# predict.py lives at the repo root (Issue #11's contract), not under
# app/ -- same sys.path pattern used in customer_repository.py and
# database/init_db.py for the same reason (direct script / uvicorn
# invocation doesn't otherwise put the repo root on sys.path).
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from predict import predict as real_predict  # noqa: E402  (see sys.path note above)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/customers", dependencies=[Depends(verify_api_key)])
def get_customers() -> list[dict[str, Any]]:
    logger.info("get_customers called (real data via CustomerRepository)")
    return CustomerRepository().get_all()


@router.get("/kpis", dependencies=[Depends(verify_api_key)])
def get_kpis() -> dict[str, Any]:
    logger.info("get_kpis called (real data via kpi_service)")
    return compute_kpis()


@router.post("/predict", response_model=CustomerPredictionResponse, dependencies=[Depends(verify_api_key)])
def predict(request: CustomerPredictionRequest) -> CustomerPredictionResponse:
    logger.info("predict called (real model via predict.py)")
    try:
        result = real_predict(request.model_dump())
    except Exception:
        # The real model can fail in ways the mock never could (e.g.
        # an unseen category the trained encoder doesn't recognize).
        # Issue #10 had no failure path here since mock_predict()
        # couldn't fail; this is new in #14 and worth a reviewer's
        # attention -- flagged in PR Notes.
        logger.exception("Real prediction failed for request")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed. See server logs for details.",
        )

    # Defensive contract check: predict.py's return shape is a locked
    # interface (Project_Specification.md section 4) that this PR does
    # not own. If it ever drifts, fail loudly here rather than let
    # FastAPI's response_model validation produce a less legible 500.
    if set(result.keys()) != {"churn_probability", "churn_prediction"}:
        logger.error("predict() returned unexpected shape: %s", result.keys())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction service returned an unexpected response shape.",
        )

    return CustomerPredictionResponse(**result)


@router.get("/model-metrics", dependencies=[Depends(verify_api_key)])
def get_model_metrics() -> dict[str, float]:
    logger.info("get_model_metrics called (real metrics via metrics_service)")
    try:
        return load_model_metrics()
    except (FileNotFoundError, ValueError):
        logger.exception("Could not load real model metrics")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model metrics are unavailable. Run the training pipeline first.",
        )