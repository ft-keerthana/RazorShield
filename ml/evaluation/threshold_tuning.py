from pathlib import Path
import argparse

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
)

from ml.data.split import split_train_validation_test


RANDOM_STATE = 42


def main():
    parser = argparse.ArgumentParser(
        description="Tune fraud classification threshold on validation data."
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to the trained model.",
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

    train_df, validation_df, test_df = (
        split_train_validation_test(
            df=df,
            target_column="is_fraud",
            random_state=RANDOM_STATE,
        )
    )

    model = joblib.load(model_path)

    X_validation = validation_df.drop(
        columns=["is_fraud"]
    )
    y_validation = validation_df["is_fraud"]

    X_test = test_df.drop(
        columns=["is_fraud"]
    )
    y_test = test_df["is_fraud"]

    validation_probabilities = model.predict_proba(
        X_validation
    )[:, 1]

    test_probabilities = model.predict_proba(
        X_test
    )[:, 1]

    # Generate candidate thresholds from the
    # observed validation probability range.
    min_probability = validation_probabilities.min()
    max_probability = validation_probabilities.max()

    thresholds = np.linspace(
        min_probability,
        max_probability,
        100,
    )

    results = []

    for threshold in thresholds:
        predictions = (
            validation_probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_validation,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_validation,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_validation,
            predictions,
            zero_division=0,
        )

        results.append(
            {
                "threshold": threshold,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
            }
        )

    results_df = pd.DataFrame(results)

    # Select threshold with the best validation F1.
    best = results_df.loc[
        results_df["f1_score"].idxmax()
    ]

    selected_threshold = float(
        best["threshold"]
    )

    # IMPORTANT:
    # The test set is untouched during threshold selection.
    test_predictions = (
        test_probabilities >= selected_threshold
    ).astype(int)

    test_precision = precision_score(
        y_test,
        test_predictions,
        zero_division=0,
    )

    test_recall = recall_score(
        y_test,
        test_predictions,
        zero_division=0,
    )

    test_f1 = f1_score(
        y_test,
        test_predictions,
        zero_division=0,
    )

    test_pr_auc = average_precision_score(
        y_test,
        test_probabilities,
    )

    print("\nThreshold Tuning Results")
    print("-" * 70)

    print(
        f"Model: {args.model}"
    )

    print(
        results_df[
            [
                "threshold",
                "precision",
                "recall",
                "f1_score",
            ]
        ].to_string(index=False)
    )

    print("\nSelected Threshold")
    print("-" * 70)

    print(
        f"Threshold:            "
        f"{selected_threshold:.6f}"
    )

    print(
        f"Validation Precision: "
        f"{best['precision']:.4f}"
    )

    print(
        f"Validation Recall:    "
        f"{best['recall']:.4f}"
    )

    print(
        f"Validation F1:        "
        f"{best['f1_score']:.4f}"
    )

    print("\nFinal Test Evaluation")
    print("-" * 70)

    print(
        f"Test PR-AUC:          "
        f"{test_pr_auc:.4f}"
    )

    print(
        f"Test Precision:       "
        f"{test_precision:.4f}"
    )

    print(
        f"Test Recall:          "
        f"{test_recall:.4f}"
    )

    print(
        f"Test F1:              "
        f"{test_f1:.4f}"
    )

    print("\nEvaluation Protocol")
    print("-" * 70)

    print(
        f"Training samples:     {len(train_df)}"
    )

    print(
        f"Validation samples:   {len(validation_df)}"
    )

    print(
        f"Test samples:         {len(test_df)}"
    )

    print(
        "Threshold selected on validation data; "
        "final metrics reported on untouched test data."
    )


if __name__ == "__main__":
    main()