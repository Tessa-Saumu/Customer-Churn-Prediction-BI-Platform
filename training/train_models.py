import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from training.train_test_split import split_training_data

# Set up logging
logger = logging.getLogger(__name__)



# Train a single model with the given name, model instance, preprocessor, and training data.
def train_single_model(
    model_name: str,
    model,
    preprocessor,
    X_train,
    y_train,
) -> Pipeline:
    # Log the start of model training
    logger.info("Training %s model...", model_name)

    # Create a pipeline that includes the preprocessor and the model
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])

    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)

    # Log the completion of model training
    logger.info("%s model training complete.", model_name)
    return pipeline


# Training multiple models and return a dictionary of trained models.
def train_models() -> tuple[dict[str, Pipeline], pd.DataFrame, pd.Series]: 
    
    # Split the training data into train and test sets
    logger.info("Splitting training data...")
    X_train, X_test, y_train, y_test, preprocessor = split_training_data()

    # Define a dictionary of models to be trained
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "XGBoost": XGBClassifier(eval_metric="logloss", random_state=42),
        "LightGBM": LGBMClassifier(random_state=42),
    }

    # Train each model and store the trained models in a dictionary
    trained_models = {}
    for model_name, model in models.items():
        trained_model = train_single_model(
            model_name,
            model,
            preprocessor,
            X_train,
            y_train,
        )
        trained_models[model_name] = trained_model

        logger.info( "%s added to trained models.", model_name)
    return trained_models, X_test, y_test

# If the script is run directly, set up logging and call the train_models function
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    trained_models, X_test, y_test = train_models()
    logger.info("All models trained successfully.")