from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

class TicketBase(BaseModel):
    category: str
    price: float
    quantity: int
    status: str = "available"

class EventCreate(BaseModel):
    marketplace_id: str  
    title: str
    venue: str
    event_date: date
    event_time: time
    poster_url: Optional[str] = None
    status: str = "published"
    tickets: List[TicketBase]