"""
ARCHIVED -- Issue #14 (Real Integration)

This file is NO LONGER USED by the application as of Issue #14.
app/api/routes.py no longer imports or calls mock_predict(). It is
retained here for reference only, per Issue #14's task list option
("Delete the file, or clearly mark it as retained reference code").

Retained rather than deleted so the scaffold-stage behavior (Issue
#10) stays visible in git history without needing to dig through old
commits, given how central this file was to the mocked stage of the
project. If the team prefers deletion instead, that's a one-line
follow-up -- flagged as a discussion point in this PR's Notes rather
than decided unilaterally here.

Original docstring below, preserved as-is:
---
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
    ARCHIVED -- not called anywhere in the app as of Issue #14.
    Returns a placeholder churn prediction. NOT a real model -- a
    fixed, deterministic heuristic so the endpoint has something
    consistent to return during scaffolding.
    """
    placeholder_probability = 0.42

    logger.info("mock_predict called (ARCHIVED -- should not be reachable in production)")

    return {
        "churn_probability": placeholder_probability,
        "churn_prediction": placeholder_probability >= CHURN_THRESHOLD,
    }