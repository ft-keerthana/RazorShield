# RazorShield Architecture

## Architecture Overview

RazorShield is designed as an event-driven risk intelligence platform.

Different merchant events require different types of risk analysis. A transaction, a return request, and a chargeback dispute should not all be processed by exactly the same model.

The platform therefore uses specialized intelligence engines that share risk context through a central Risk Orchestrator.

## High-Level Architecture

```mermaid
flowchart TD

    A[Merchant Event Sources]

    A --> B[Transaction Events]
    A --> C[Return Events]
    A --> D[Dispute / Chargeback Events]

    B --> E[Feature & Signal Engine]
    E --> F[Rule-Based Risk Signals]
    E --> G[Fraud ML Model]

    F --> H[Risk Orchestrator]
    G --> H

    C --> I[Return Risk Engine]
    I --> H

    D --> J[Chargeback Evidence Responder]

    K[Fraud-Spike Detector] --> H
    L[Abuse-Ring Sentinel] --> H

    B --> K
    B --> L

    H --> M[Policy / Decision Engine]

    M --> N[ALLOW]
    M --> O[REVIEW / VERIFY]
    M --> P[HOLD / BLOCK]

    O --> Q[Investigation & Explainability]
    P --> Q

    Q --> R[Human / Merchant Action]

    J --> S[AI-Assisted Evidence Response]

    N --> T[Outcomes & Feedback]
    R --> T
    S --> T

    T --> U[Label / Feedback Store]
    U --> V[Model & Rule Evaluation]
    V --> W[Continuous Improvement]