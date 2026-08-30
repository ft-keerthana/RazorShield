from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Decision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    HOLD = "hold"
    BLOCK = "block"


class RiskDecision(BaseModel):
    event_id: str
    event_type: str

    risk_score: float = Field(..., ge=0, le=100)

    decision: Decision
    reasons: list[str] = Field(default_factory=list)

    created_at: datetime