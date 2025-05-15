from pydantic import BaseModel
from typing import Optional

class WeeklyReportDTO(BaseModel):
    week: str  # YYYY-WW
    overrun_threshold: int
    overrun_days: int
    most_warned_app: Optional[str]
    scroll_distance_m: float
    goal_achieved: bool
    summary: str
    most_difficult_day: Optional[str]
    alerts_total: int
    top_used_app: Optional[str]

class WeeklyReportSummaryDTO(BaseModel):
    week: str
    summary: str