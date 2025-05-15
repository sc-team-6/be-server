from pydantic import BaseModel, Field
from typing import Optional

class WeeklyReport(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    week: str  # "2025-W15"
    overrun_threshold: int
    overrun_days: int
    most_warned_app: Optional[str]
    scroll_distance_m: float
    goal_achieved: bool
    summary: str
    most_difficult_day: Optional[str]
    alerts_total: int
    top_used_app: Optional[str]