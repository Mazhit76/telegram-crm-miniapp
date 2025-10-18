from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LeadCreate(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    phone: Optional[str] = None
    budget: Optional[str] = None
    project_type: str
    description: str

class ProjectCalculation(BaseModel):
    description: str
    features: List[str]
    budget_range: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class LeadResponse(BaseModel):
    id: int
    status: str
    project_type: str
    description: str
    created_at: datetime
    
    class Config:
        from_attributes = True