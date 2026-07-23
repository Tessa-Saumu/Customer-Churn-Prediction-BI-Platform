from pathlib import Path
from typing import Any

import sys
import joblib
import logging
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from training.preprocessing import prepare_features

MODEL_PATH = REPO_ROOT / "models" / "best_model.pkl"
logger = logging.getLogger(__name__)
# Load the trained model
logger.info("Loading trained model from %s", MODEL_PATH)
model = joblib.load(MODEL_PATH)


def predict(customer_data: dict[str, Any]) -> dict[str, Any]:

    """
    Generate a churn prediction for a single customer.

    Args:
        customer_data: Raw customer attributes.

    Returns:
        Dictionary containing churn probability and prediction.
    """  
    logger.info("Generating churn prediction...")
    X = pd.DataFrame([customer_data])

    logger.info("Preparing features for prediction.")
    X = prepare_features(X)

    probability = float(model.predict_proba(X)[0][1])
    prediction = bool(model.predict(X)[0])

    logger.info("Prediction complete. Probability=%.4f Prediction=%s", probability, prediction)
    return {
        "churn_probability": probability,
        "churn_prediction": prediction,
    }