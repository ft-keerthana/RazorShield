from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class ReturnReason(str, Enum):
    DAMAGED = "damaged"
    WRONG_ITEM = "wrong_item"
    NOT_AS_DESCRIBED = "not_as_described"
    CHANGED_MIND = "changed_mind"
    OTHER = "other"


class ReturnEvent(BaseModel):
    return_id: str
    transaction_id: str
    customer_id: str
    merchant_id: str

    reason: ReturnReason
    requested_at: datetime
    amount: Decimal
