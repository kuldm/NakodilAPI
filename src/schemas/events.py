from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    location_id: int
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=100)
    starts_at: datetime
    base_price: int = Field(gt=0)


class EventRead(BaseModel):
    id: int
    organizer_id: int
    location_id: int
    title: str
    description: str | None
    category: str
    starts_at: datetime
    base_price: int

    model_config = ConfigDict(from_attributes=True)


class EventAdd(EventCreate):
    organizer_id: int

    model_config = ConfigDict(from_attributes=True)
