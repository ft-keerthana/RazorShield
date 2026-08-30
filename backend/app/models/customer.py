from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Customer(BaseModel):
    customer_id: str = Field(..., description="Unique customer identifier")
    email: str
    account_created_at: datetime
    country: str = Field(..., min_length=2, max_length=2)