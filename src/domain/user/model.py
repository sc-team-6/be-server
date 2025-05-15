from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    username: str
    hashed_password: str

    # Onboarding 설정 정보
    avg_screen_time: Optional[str] = None  # "less_than_2h", "3-4h", ...
    usage_type_to_reduce: Optional[List[str]] = []
    usage_reduction_goal: Optional[str] = None  # "a_lot", "a_little", "same"
    calendar_permission_granted: Optional[bool] = False
    sleep_time_range: Optional[Dict[str, str]] = {"start": "22:00", "end": "07:00"}
    initial_overrun_threshold: Optional[int] = 80
    onboarding_completed: Optional[bool] = False