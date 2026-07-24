import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sklearn.model_selection import train_test_split

from training.preprocessing import (
    prepare_training_data,
    build_preprocessor,
)

# Set up logging
logger = logging.getLogger(__name__)

"""Constants for train-test split, Test size is set to 20% of the dataset, 
    and random state is set for reproducibility"""
TEST_SIZE = 0.2
RANDOM_STATE = 42

""" split_training_data function is responsible for preparing the training data, 
building the preprocessor, and splitting the data into train and test sets. 
It returns the train and test sets along with the preprocessor."""
def split_training_data():
    logger.info("Preparing training data...")
    X, y = prepare_training_data()

    logger.info("Building preprocessor...")
    preprocessor = build_preprocessor(X)

    logger.info("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    logger.info(
    "Training samples: %d | Test samples: %d",
    len(X_train),
    len(X_test),
                )
    
    return (
    X_train,
    X_test,
    y_train,
    y_test,
    preprocessor,
)

# If the script is run directly, set up logging and call the split_training_data function
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    split_training_data()