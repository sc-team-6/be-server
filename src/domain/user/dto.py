from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
class UserRegisterDTO(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(BaseModel):
    id: str
    email: EmailStr
    username: str

class UserSettingUpdateDTO(BaseModel):
    avg_screen_time: Optional[str]
    usage_type_to_reduce: Optional[List[str]]
    usage_reduction_goal: Optional[str]
    calendar_permission_granted: Optional[bool]
    sleep_time_range: Optional[Dict[str, str]]
    initial_overrun_threshold: Optional[int]
    onboarding_completed: Optional[bool]