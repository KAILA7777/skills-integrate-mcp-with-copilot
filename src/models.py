from typing import Dict, List
from pydantic import BaseModel, Field, RootModel


class Activity(BaseModel):
    description: str
    schedule: str
    max_participants: int = Field(..., ge=0)
    participants: List[str] = Field(default_factory=list)


class ActivityStore(RootModel[Dict[str, Activity]]):
    root: Dict[str, Activity]
