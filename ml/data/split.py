from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split


def split_train_test(
    df: pd.DataFrame,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Create reproducible train/test splits while preserving
    the class distribution of the target variable.
    """

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def split_train_validation_test(
    df: pd.DataFrame,
    target_column: str,
    train_size: float = 0.6,
    validation_size: float = 0.2,
    random_state: int = 42,
):
    """
    Create reproducible train/validation/test splits.

    The final test set remains completely separate from
    model fitting and threshold selection.
    """

    train_df, temp_df = train_test_split(
        df,
        train_size=train_size,
        random_state=random_state,
        stratify=df[target_column],
    )

    validation_relative_size = validation_size / (
        1.0 - train_size
    )

    validation_df, test_df = train_test_split(
        temp_df,
        train_size=validation_relative_size,
        random_state=random_state,
        stratify=temp_df[target_column],
    )

    return train_df, validation_df, test_df