# RazorShield Design Goals

## 1. Minimize Financial Loss Without Excessive False Positives

The goal is not to block the maximum possible number of suspicious transactions.

Blocking legitimate customers creates lost revenue and damages customer experience.

RazorShield therefore evaluates both fraud detection performance and the cost of false positives.

## 2. Prefer Explainable Decisions

Risk decisions should provide understandable reasons.

A merchant should be able to determine why an event was flagged and what action is recommended.

## 3. Use the Right Intelligence for the Right Problem

Different risk problems require different approaches.

- Rules are useful for known patterns.
- Machine learning is useful for complex feature combinations.
- Anomaly detection is useful for emerging attacks.
- Graph analysis is useful for coordinated abuse.
- AI-assisted retrieval is useful for unstructured chargeback evidence.

## 4. Separate Risk Scoring From Irreversible Actions

Risk can be continuously measured without immediately blocking a customer.

Irreversible or high-value actions should use explicit policy controls and, when appropriate, human review.

## 5. Design for Delayed Labels

Fraud and chargeback labels may arrive weeks or months after the original transaction.

The system should therefore support faster proxy signals and clearly distinguish between immediate outcomes and delayed ground-truth labels.

## 6. Measure Performance Honestly

Models should be evaluated on held-out data using metrics appropriate for imbalanced datasets.

Metrics may include:

- Precision
- Recall
- PR-AUC
- False-positive rate
- Business cost

## 7. Build a Modular System

Individual risk engines should be independently testable and extensible.

This allows new signals and models to be introduced without redesigning the entire platform.