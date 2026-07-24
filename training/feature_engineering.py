"""Feature engineering utilities.
Creating additional features to be used during model training. """


from __future__ import annotations
import pandas as pd
import logging

logger = logging.getLogger(__name__)


"""In this function, I create a new feature called "TenureBucket" that groups customers
  into different tenure ranges based on their tenure in months. The function takes a
  DataFrame as input and returns a modified DataFrame with the new feature added."""

def add_tenure_bucket(df: pd.DataFrame) -> pd.DataFrame:
    #Create tenure groups from tenure_months
    bins = [-1, 12, 24, 48, 72]

    labels = [
        "0-12",
        "13-24",
        "25-48",
        "49+",
    ]

    df = df.copy()
    df["TenureBucket"] = pd.cut(
        df["tenure_months"],
        bins=bins,
        labels=labels,
    )

    return df


""" In this function, I create a new feature called "TotalServicesCount" that counts 
the number of services a customer has subscribed to. The function takes a DataFrame 
as input and returns a modified DataFrame with the new feature added"""
def add_total_services_count(df: pd.DataFrame) -> pd.DataFrame:
    
    #Count the number of subscribed services.
    service_columns = [
        "phone_service",
        "multiple_lines",
        "online_security",
        "online_backup",
        "device_protection",
        "tech_support",
        "streaming_tv",
        "streaming_movies",
    ]

    df = df.copy()

    df["TotalServicesCount"] = (
        df[service_columns]
        .eq("Yes")
        .sum(axis=1)
    )

    return df


"""In this function, I create a new feature called "AvgMonthlySpend" that estimates the
   average monthly spend of a customer over their lifetime. The function takes a DataFrame
     as input and returns a modified DataFrame with the new feature added."""
def add_average_monthly_spend(df: pd.DataFrame) -> pd.DataFrame:
    
    #Replace zero tenure with 1 to avoid division-by-zerofor newly joined customers.
    df = df.copy()

    df["AvgMonthlySpend"] = (
        df["total_charges"]
        / df["tenure_months"].replace(0, 1)
    )

    return df


# Apply all feature engineering steps.  
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    
    logger.info("Applying feature engineering.")
    df = add_tenure_bucket(df)
    df = add_total_services_count(df)
    df = add_average_monthly_spend(df)
    
    logger.info(
    "Feature engineering complete. Dataset now has %d columns.",
    len(df.columns),
)

    return df



