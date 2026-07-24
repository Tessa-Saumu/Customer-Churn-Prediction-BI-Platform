import logging
import sys
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from training.data_loader import load_training_data
from training.feature_engineering import engineer_features

# Set up logging
logger = logging.getLogger(__name__)

# Columns to drop from the dataset before training
DROP_COLUMNS = [
    "customer_id",
    "country",
    "state",
    "city",
    "zip_code",
    "lat_long",
    "latitude",
    "longitude",
    "churn_label",
    "churn_reason",
    "cltv",
    "churn_score",
]

"""
Columns removed before training includes:

- customer_id:
    Identifier only.

- Geographic columns:
    Removed because they add little predictive value for this dataset
    and unnecessarily increase dimensionality.

churn_label:
    Text version of the target.

- churn_reason:
    Known only after churn occurs, so using it would leak future information.

- churn_score:
    IBM Cognos-computed churn risk score, derived from the churn
    outcome itself -- same leakage reasoning as churn_reason and cltv.
    A real customer being scored through /predict has no
    Cognos-generated churn_score yet, so the model can never receive
    this at real prediction time; training on it teaches the model to
    lean on a signal that structurally doesn't exist outside this
    dataset. Flagged during Issue #14 integration testing: the
    ColumnTransformer, fit with churn_score present, rejected any
    real single-record prediction request with
    "ValueError: columns are missing: {'churn_score'}" -- confirming
    this was missing from the original leakage-column review, not an
    intentional inclusion.

- cltv:
    Customer Lifetime Value is calculated using business rules that
    reflect future customer value and therefore introduces data leakage.
"""


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
        Apply the same feature engineering and column removal
        used before both model training and prediction.
    """
    logger.info("Preparing model features....")
    df = engineer_features(df)
    df = df.drop(
        columns=DROP_COLUMNS,
        errors="ignore",
    )
    logger.info("Prepared features with %d samples and %d features.", len(df), df.shape[1])
    return df

#Load the customer data and prepare the features and target variable for model training.
def prepare_training_data() -> tuple[pd.DataFrame, pd.Series]:
    
    logger.info("Loading and preparing training data...")
    df = load_training_data()
    df = prepare_features(df)
    y = df["churn_value"]
    X = df.drop(columns=["churn_value"])
    logger.info("Prepared dataset with %d samples and %d features.",len(X),X.shape[1],)
    return X, y


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    Build the preprocessing transformer used during model training.
    """

    categorical_columns = (
        X.select_dtypes(include=["object", "category", "string"])
        .columns
        .tolist())

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns,
            ),
        ],
        remainder="passthrough",
    )

    logger.info("Built preprocessor with %d features.", X.shape[1])

    return preprocessor


# To check if this script is running directly, executing the data preparation function and printing the results
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    X, y = prepare_training_data()

    logger.info("\n%s", X.head())
    logger.info("\n%s", y.head())