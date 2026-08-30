from datetime import datetime

from pydantic import BaseModel, Field


class Device(BaseModel):
    device_id: str = Field(..., description="Unique device identifier")
    ip_address: str
    country: str = Field(..., min_length=2, max_length=2)
    user_agent: str | None = None
    first_seen_at: datetime | None = None
