from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class LogItemDTO(BaseModel):
    app_package: str
    total_minutes: int
    notification_shown: bool
    notification_accepted: Optional[bool]
    location_zone: str
    is_overuse: bool

class LogCreateRequest(BaseModel):
    date: date
    logs: List[LogItemDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-04-10",
                "logs": [
                    {
                        "app_package": "com.youtube.android",
                        "total_minutes": 68,
                        "notification_shown": True,
                        "notification_accepted": False,
                        "location_zone": "home",
                        "is_overuse": True
                    }
                ]
            }
        }

class LogResponse(BaseModel):
    status: str
    message: str