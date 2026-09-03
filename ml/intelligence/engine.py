from __future__ import annotations

import pandas as pd

from ml.intelligence.behavioral import add_behavioral_features
from ml.intelligence.device import add_device_entity_features
from ml.intelligence.location import add_location_features
from ml.intelligence.rules import apply_risk_rules


def build_risk_intelligence(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the complete RazorShield risk intelligence feature set.
    """

    data = df.copy()

    data = add_behavioral_features(data)
    data = add_location_features(data)
    data = add_device_entity_features(data)
    data = apply_risk_rules(data)

    return data
