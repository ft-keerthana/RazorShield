from __future__ import annotations

import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic transaction data cleaning.
    """

    data = df.copy()

    # Remove duplicate records
    data = data.drop_duplicates()

    # Normalize column names
    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return data


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values using simple baseline strategies.

    Numeric columns are filled with their median.
    Categorical columns are filled with 'unknown'.
    """

    data = df.copy()

    numeric_columns = data.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = data.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    for column in numeric_columns:
        data[column] = data[column].fillna(data[column].median())

    for column in categorical_columns:
        data[column] = data[column].fillna("unknown")

    return data