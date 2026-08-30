from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    merchant_id: str

    amount: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)

    status: TransactionStatus
    timestamp: datetime

    billing_country: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )
    shipping_country: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )

    device_id: str | None = None
    ip_address: str | None = None