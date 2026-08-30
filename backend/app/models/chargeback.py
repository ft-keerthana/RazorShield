from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class ChargebackReason(str, Enum):
    FRAUD = "fraud"
    DUPLICATE = "duplicate"
    PRODUCT_NOT_RECEIVED = "product_not_received"
    PRODUCT_UNACCEPTABLE = "product_unacceptable"
    OTHER = "other"


class Chargeback(BaseModel):
    chargeback_id: str
    transaction_id: str
    customer_id: str
    merchant_id: str

    amount: Decimal
    reason: ChargebackReason

    opened_at: datetime
    due_at: datetime | None = None