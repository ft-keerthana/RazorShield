from pathlib import Path
import argparse

import joblib
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    classification_report,
    precision_score,
    recall_score,
    roc_auc_score,
)

from ml.data.split import split_train_validation_test


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a trained fraud detection model."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to the trained model.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Classification threshold. Default: 0.5",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]

    data_path = (
        project_root
        / "data"
        / "processed"
        / "transactions_processed.csv"
    )

    model_path = project_root / args.model

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    df = pd.read_csv(data_path)

    _, _, test_df = split_train_validation_test(
        df=df,
        target_column="is_fraud",
    )

    X_test = test_df.drop(columns=["is_fraud"])
    y_test = test_df["is_fraud"]

    model = joblib.load(model_path)

    probabilities = model.predict_proba(X_test)[:, 1]

    predictions = (
        probabilities >= args.threshold
    ).astype(int)

    print("\nModel Evaluation")
    print("-" * 40)

    print(f"Model: {model_path}")
    print(f"Threshold: {args.threshold:.6f}")
    print(f"Test samples: {len(test_df)}")
    print(f"Test frauds: {int(y_test.sum())}")

    print(
        f"Precision: "
        f"{precision_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"Recall: "
        f"{recall_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"ROC-AUC: "
        f"{roc_auc_score(y_test, probabilities):.4f}"
    )

    print(
        f"PR-AUC: "
        f"{average_precision_score(y_test, probabilities):.4f}"
    )

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()