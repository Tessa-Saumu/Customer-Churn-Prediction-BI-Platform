"""
Issue #10 -- FastAPI Scaffold -- app/services/mock_prediction_service.py

TEMPORARY. This is explicitly a placeholder per the issue -- it exists
so /predict has something to call before Latifah's real model exists
(Issue #11) and before Issue #14 wires it in for real. Nothing here is
a real prediction.

When Issue #14 happens, this gets swapped for a call to the real
predict() in repo-root predict.py. The output shape below matches that
contract exactly -- {"churn_probability": float,
"churn_prediction": bool} -- so the swap doesn't require touching
routes.py or the response schema.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

CHURN_THRESHOLD = 0.5


def mock_predict(customer_data: dict[str, Any]) -> dict[str, Any]:
    """
    Returns a placeholder churn prediction. NOT a real model -- a
    fixed, deterministic heuristic so the endpoint has something
    consistent to return during scaffolding.
    """
    # TEMPORARY / PLACEHOLDER -- replace in Issue #14 with a call to
    # the real predict() from repo-root predict.py (Latifah, Issue #11).
    placeholder_probability = 0.42

    logger.info("mock_predict called (placeholder, not a real model)")

    return {
        "churn_probability": placeholder_probability,
        "churn_prediction": placeholder_probability >= CHURN_THRESHOLD,
    }