from dataclasses import dataclass

from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass
class EvaluationResult:
    threshold: float
    test_samples: int
    fraud_cases: int
    precision: float
    recall: float
    f1: float
    roc_auc: float
    pr_auc: float


def evaluate_predictions(
    y_true,
    probabilities,
    threshold: float,
) -> EvaluationResult:
    """
    Evaluate fraud predictions on a held-out dataset.

    The threshold should be selected using validation data,
    not the held-out test set.
    """

    predictions = (
        probabilities >= threshold
    ).astype(int)

    return EvaluationResult(
        threshold=round(float(threshold), 6),
        test_samples=len(y_true),
        fraud_cases=int(sum(y_true)),
        precision=round(
            float(
                precision_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            ),
            4,
        ),
        recall=round(
            float(
                recall_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            ),
            4,
        ),
        f1=round(
            float(
                f1_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            ),
            4,
        ),
        roc_auc=round(
            float(
                roc_auc_score(
                    y_true,
                    probabilities,
                )
            ),
            4,
        ),
        pr_auc=round(
            float(
                average_precision_score(
                    y_true,
                    probabilities,
                )
            ),
            4,
        ),
    )