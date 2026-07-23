import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


import pandas as pd
from typing import Tuple
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

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

- cltv:
    Customer Lifetime Value is calculated using business rules that
    reflect future customer value and therefore introduces data leakage.
"""


"""
    Load, engineer and preprocess the customer churn dataset
    for model training.
    """
def prepare_training_data() -> tuple[np.ndarray, pd.Series, Pipeline]:
    
    # Load training data from the SQLite database   
    logger.info("Loading training data from SQLite database.")
    df = load_training_data()

    # Engineer features
    logger.info("Applying engineered features.")
    df = engineer_features(df)

    #Separating target
    y = df["churn_value"]

    #Separating features
    X = df.drop(columns=DROP_COLUMNS + ["churn_value"])

    # Define categorical features for one-hot encoding
    categorical_columns = (
    X.select_dtypes(include=["object", "category", "string"])
    .columns
    .tolist()
)
    
    # Create a preprocessing pipeline for categorical features
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

    logger.info(
    "Prepared dataset with %d samples and %d features.",
    len(X),
    X.shape[1],
)
    return X, y


"""
    Build a preprocessing pipeline for the customer churn dataset.
    Returns a sklearn Pipeline object that can be used to transform new data.
    """
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:

    # Define categorical features for one-hot encoding
    categorical_columns = (
        X.select_dtypes(include=["object", "category", "string"])
        .columns
        .tolist()
    )

    # Create a preprocessing pipeline for categorical features
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

    logger.info(
        "Built preprocessor with %d features.",
        X.shape[1],
    )
    
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
