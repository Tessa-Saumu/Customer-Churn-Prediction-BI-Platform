import logging
import sys
from pathlib import Path
from sklearn.base import ClassifierMixin

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from typing import Any
import pandas as pd
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
)

from training.train_models import train_models

# Set up logging
logger = logging.getLogger(__name__)
# Model directory
MODEL_PATH = REPO_ROOT / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# Define a function to evaluate a single model
def evaluate_model(
    model_name: str,
    model: ClassifierMixin,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, Any]:
    """
    Evaluate a trained model on the test set and return evaluation metrics.
    """
    logger.info("Evaluating %s model...", model_name)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)

    logger.info(
        "%s model evaluation complete. Accuracy: %.4f, Precision: %.4f, Recall: %.4f, ROC AUC: %.4f",
        model_name,
        accuracy,
        precision,
        recall,
        roc_auc,
    )

    return {
        "model_name": model_name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "roc_auc": roc_auc,
        "confusion_matrix": conf_matrix.tolist(),
    }
    
# Define a function to evaluate all models
def evaluate_all_models() -> pd.DataFrame:
    """
    Train and evaluate all models, returning a DataFrame with evaluation metrics.
    """
    logger.info("Training models...")
    trained_models, X_test, y_test = train_models()

    evaluation_results = []
    for model_name, model in trained_models.items():
        metrics = evaluate_model(model_name, model, X_test, y_test)
        metrics["model_name"] = model_name  # Add model name to the metrics dictionary
        evaluation_results.append(metrics)

    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(evaluation_results)
    logger.info("All models evaluated. Results:\n%s", results_df)


    # Identify the best model based on ROC AUC score
    best_model_name = results_df.sort_values(
    by="roc_auc",
    ascending=False,
    ).iloc[0]["model_name"]

    logger.info("Best model: %s", best_model_name)
    best_model = trained_models[best_model_name]

    # save model
    joblib.dump(
    best_model,
    MODEL_PATH / "best_model.pkl",
    )

    logger.info(
    "Best model (%s) saved successfully.",
    best_model_name,
                )
    logger.info("Evaluation complete.\n%s", results_df)

    # Generate a markdown report for model comparison
    REPORT_DIR = Path("evaluation")
    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / "model_comparison.md"
    with report_path.open("w", encoding="utf-8") as file:
        file.write("# Customer Churn Model Comparison\n\n")
        file.write(results_df.to_markdown(index=False))
        file.write("\n\n## Selected Model\n\n")
        file.write(f"**{best_model_name}**\n\n")

        # Write the performance metrics of the best model
        best_metrics = results_df.loc[
        results_df["model_name"] == best_model_name
                                ].iloc[0]
        
        file.write("### Performance\n\n")
        file.write(f"- Accuracy: {best_metrics['accuracy']:.4f}\n")
        file.write(f"- Precision: {best_metrics['precision']:.4f}\n")
        file.write(f"- Recall: {best_metrics['recall']:.4f}\n")
        file.write(f"- ROC AUC: {best_metrics['roc_auc']:.4f}\n")
        file.write(f"- Confusion Matrix: {best_metrics['confusion_matrix']}\n\n")

        file.write("## Why this model was selected\n\n")
        file.write(
    f"{best_model_name} was selected because it achieved the highest ROC AUC "
    f"({best_metrics['roc_auc']:.4f}), which was the primary model selection "
    "criterion. It also demonstrated strong overall performance across "
    "accuracy, precision, and recall, making it the best balance of predictive "
    "performance among the evaluated models."
)
    
    return results_df




    
# If the script is run directly, set up logging and call the evaluate_all_models function
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    results = evaluate_all_models()
    logger.info("\n%s", results)