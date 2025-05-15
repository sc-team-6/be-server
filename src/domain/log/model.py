from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AppLog(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    date: date
    app_package: str
    total_minutes: int
    notification_shown: bool
    notification_accepted: Optional[bool]
    location_zone: str
    is_overuse: bool