"""
Issue #11 -- Model Training & Evaluation -- predict.py

Issue #14 changes (flagged per spec "Notes" convention -- coordinate
with Latifah before merging):

1. MODEL_PATH is now read from the MODEL_PATH environment variable,
   falling back to the original repo-root-relative default if unset.
   Reason: acceptance criteria for Issue #14 requires "All model
   artifact paths are configurable and do not depend on one
   developer's machine."

2. NEW: _adapt_api_fields_to_training_schema(), called at the top of
   predict(). See its own docstring below for the full "why" -- short
   version: CustomerPredictionRequest (Praise, #10) uses the raw
   Telco CSV's field names/casing (tenure, SeniorCitizen,
   MonthlyCharges...), but training/feature_engineering.py (Latifah,
   #11) expects Mercy's cleaned DB column names (tenure_months,
   senior_citizen, monthly_charges...), because it's built to run on
   CustomerRepository output. Nothing reconciled these until now --
   this was surfaced by a live 500 (KeyError: 'tenure_months') on
   POST /predict during Issue #14 verification, not caught by any
   earlier review, since Issue #10's mock never touched real feature
   engineering and Issue #11's training pipeline never went through
   the API schema.

   This is exactly the "format differs" case the issue anticipated:
   "Coordinate with Latifah to update predict.py, or add a thin
   adapter layer in the API. Do not change the public API contract."
   Renaming CustomerPredictionRequest's fields would break the public
   contract Issue #14 must preserve, so this is that adapter --
   placed here rather than in routes.py, since this is specifically
   the boundary between the two schemas and routes.py shouldn't need
   to know Latifah's internal column names.

   predict()'s own signature and return shape are unchanged -- only
   an internal translation step was added before prepare_features().

Everything else in this file is untouched from Issue #11's original.
"""

import os
from pathlib import Path
from typing import Any

import sys
import joblib
import logging
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from training.preprocessing import prepare_features

# CHANGED (Issue #14): configurable via MODEL_PATH env var, default
# unchanged from Issue #11.
MODEL_PATH = Path(os.environ.get("MODEL_PATH", str(REPO_ROOT / "models" / "best_model.pkl")))

logger = logging.getLogger(__name__)
# Load the trained model
logger.info("Loading trained model from %s", MODEL_PATH)
model = joblib.load(MODEL_PATH)


# NEW (Issue #14): maps CustomerPredictionRequest's field names (raw
# Telco CSV convention) to Mercy's finalized DB column names (sql/schema.sql),
# which is what training/feature_engineering.py expects since it's
# built against CustomerRepository output, not the API schema.
#
# VERIFY BEFORE MERGE: this list was built by reading sql/schema.sql
# directly, not by inspecting a populated database. Confirm every
# right-hand name below matches your actual `customers` table columns
# 1:1 -- e.g. via `PRAGMA table_info(customers);` -- before relying on
# this in production.
_API_FIELD_TO_DB_COLUMN: dict[str, str] = {
    "gender": "gender",
    "SeniorCitizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "tenure": "tenure_months",
    "PhoneService": "phone_service",
    "MultipleLines": "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity": "online_security",
    "OnlineBackup": "online_backup",
    "DeviceProtection": "device_protection",
    "TechSupport": "tech_support",
    "StreamingTV": "streaming_tv",
    "StreamingMovies": "streaming_movies",
    "Contract": "contract",
    "PaperlessBilling": "paperless_billing",
    "PaymentMethod": "payment_method",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
}


def _adapt_api_fields_to_training_schema(customer_data: dict[str, Any]) -> dict[str, Any]:
    """
    Translates a CustomerPredictionRequest-shaped dict (API field
    names) into the column names/value conventions
    training/feature_engineering.py expects (Mercy's DB schema).

    Two kinds of translation happen here:
    1. Renaming: e.g. "tenure" -> "tenure_months".
    2. Value normalization: sql/schema.sql stores senior_citizen as
       TEXT, but CustomerPredictionRequest.SeniorCitizen is an int
       (0/1) matching the raw CSV's original encoding. Converted to
       "Yes"/"No" strings here to match what CustomerRepository (and
       therefore the data feature_engineering.py was built against)
       actually returns -- confirmed against the real database via
       `SELECT DISTINCT senior_citizen FROM customers;`, which
       returned exactly {"Yes", "No"}.

    Raises:
        KeyError: if customer_data is missing a field this mapping
            expects -- surfaces clearly rather than silently dropping
            a column feature_engineering.py will later need.
    """
    adapted: dict[str, Any] = {}
    for api_field, db_column in _API_FIELD_TO_DB_COLUMN.items():
        adapted[db_column] = customer_data[api_field]

    # Value normalization: int 0/1 -> the DB's stored TEXT convention
    # (confirmed Yes/No against the real database, see docstring above).
    senior_citizen_map = {0: "No", 1: "Yes"}
    adapted["senior_citizen"] = senior_citizen_map[adapted["senior_citizen"]]

    return adapted


def predict(customer_data: dict[str, Any]) -> dict[str, Any]:

    """
    Generate a churn prediction for a single customer.

    Args:
        customer_data: Raw customer attributes, in
            CustomerPredictionRequest's field-name convention (the
            locked API request schema).

    Returns:
        Dictionary containing churn probability and prediction.
    """  
    logger.info("Generating churn prediction...")

    # NEW (Issue #14): translate API field names to the DB/training
    # column convention before feature engineering runs on it.
    training_shaped_data = _adapt_api_fields_to_training_schema(customer_data)
    X = pd.DataFrame([training_shaped_data])

    logger.info("Preparing features for prediction.")
    X = prepare_features(X)

    probability = float(model.predict_proba(X)[0][1])
    prediction = bool(model.predict(X)[0])

    logger.info("Prediction complete. Probability=%.4f Prediction=%s", probability, prediction)
    return {
        "churn_probability": probability,
        "churn_prediction": prediction,
    }