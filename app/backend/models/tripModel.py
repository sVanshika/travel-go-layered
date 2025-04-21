from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripBase(BaseModel):
    destination: str
    days: int
    itinerary: str
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    tripId: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True 