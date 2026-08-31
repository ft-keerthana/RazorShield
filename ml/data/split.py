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