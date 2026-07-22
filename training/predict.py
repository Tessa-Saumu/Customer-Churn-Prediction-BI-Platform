from pathlib import Path
from typing import Any

import sys
import joblib
import logging
import pandas as pd
from sklearn.pipeline import Pipeline

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

MODEL_PATH = REPO_ROOT / "models" / "best_model.pkl"
logger = logging.getLogger(__name__)


logger.info("Loading trained model...")
model = joblib.load(MODEL_PATH)

def predict(customer_data: dict[str, Any]) -> dict[str, Any]:
    
    logger.info("Generating churn prediction...")
    X = pd.DataFrame([customer_data])

    churn_probability = float(model.predict_proba(X)[0][1])
    churn_prediction = bool(model.predict(X)[0])

    logger.info(
        "Prediction complete. Probability=%.4f Prediction=%s",
        churn_probability,
        churn_prediction,
    )
    return {
        "churn_probability": churn_probability,
        "churn_prediction": churn_prediction,
    }