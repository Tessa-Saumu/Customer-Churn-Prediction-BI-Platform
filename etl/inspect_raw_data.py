#Import relevant libraries

import pandas as pd
from pathlib import Path

DATASET_PATH = "data/raw/telco_customer_churn.csv"

#Loading The Data Set

def load_data(path: str) -> pd.DataFrame:
  
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {file_path.resolve()}"
        )

    df = pd.read_csv(file_path)
    print("Dataset loaded successfully.")


    return df

#Inspecting Data to Understand

def inspect_data(df: pd.DataFrame) -> None:
  
    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names")
    print("-" * 60)
    print(df.columns.tolist())

    print("\nData Types")
    print("-" * 60)
    print(df.dtypes)

    print("\nMissing Values")
    print("-" * 60)
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print("-" * 60)
    print(df.duplicated().sum())

    print("\nUnique Values Per Column")
    print("-" * 60)
    print(df.nunique())

    print("\nSummary Statistics")
    print("-" * 60)
    print(df.describe(include="all"))

#Cleaning Data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
   

    # Created a copy to avoid modifying the original DataFrame

    df = df.copy()

    
    # Standardized column names
  
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("Column names standardized.")

   
    # Removed whitespaces
   
    object_columns = df.select_dtypes(include="object").columns

    for col in object_columns:
        df[col] = df[col].str.strip()

    print("Removed extra whitespace from string columns.")

   
    # Removed duplicate rows
   
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicate_count} duplicate rows.")
    else:
        print("No duplicate rows found.")

    
    # Converted total_charges to numeric
   
    df["total_charges"] = pd.to_numeric(
        df["total_charges"],
        errors="coerce"
    )

    print("Converted total_charges to numeric.")

   
    # Handled missing values
    
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # Churn reason is only applicable to customers who churned

    df["churn_reason"] = df["churn_reason"].fillna("Not Applicable")

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nDataset cleaned successfully.")

    return df

#Validation of the data

def validate_data(df: pd.DataFrame) -> None:
  

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        print("No duplicate rows found.")
    else:
        print(f"{duplicates} duplicate rows found.")

    # Missing values

    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("No missing values found.")
    else:
        print("\nColumns with missing values:")
        print(missing[missing > 0])

    # Total charges data type

    if pd.api.types.is_numeric_dtype(df["total_charges"]):
        print(" total_charges is numeric.")
    else:
        print(" total_charges is not numeric.")

    # Churn value

    valid_values = set(df["churn_value"].unique())

    if valid_values.issubset({0, 1}):
        print("churn_value contains valid values.")
    else:
        print("Invalid values found in churn_value.")

    # Negative charges

    if (df["monthly_charges"] < 0).any():
        print("Negative monthly charges found.")
    else:
        print("Monthly charges are valid.")

    if (df["total_charges"] < 0).any():
        print("Negative total charges found.")
    else:
        print("Total charges are valid.")

    print("\nValidation complete.")

#Main code
#    
if __name__ == "__main__":

    #Loading CSV file

    df = load_data(DATASET_PATH)

    #Inspect

    inspect_data(df)

    # Transform
   
    cleaned_df = clean_data(df)

    # Validate
    
    validate_data(cleaned_df)

    # Load clean dataset
    
    output_directory = Path("data/processed")
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "cleaned_telco_customer_churn.csv"

    cleaned_df.to_csv(output_file, index=False)


   