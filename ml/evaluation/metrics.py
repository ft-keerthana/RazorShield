from typing import Any

from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


def calculate_classification_metrics(
    y_true: Any,
    y_pred: Any,
    y_score: Any | None = None,
) -> dict[str, float]:
    """
    Calculate evaluation metrics for fraud detection.

    Accuracy is intentionally not the primary metric because fraud datasets
    are typically highly imbalanced.
    """

    metrics = {
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "f1_score": float(
            f1_score(y_true, y_pred, zero_division=0)
        ),
    }

    if y_score is not None:
        metrics["average_precision"] = float(
            average_precision_score(y_true, y_score)
        )

        metrics["roc_auc"] = float(
            roc_auc_score(y_true, y_score)
        )

    return metrics


def get_confusion_matrix(
    y_true: Any,
    y_pred: Any,
) -> dict[str, int]:
    """Return fraud detection confusion matrix values."""

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }