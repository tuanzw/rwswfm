from pydantic import BaseModel, Field
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[int] = Field(None)
    name: str = Field(..., max_length=50, pattern=r'^[0-9a-zA-Z-]*$')
    active: bool = True

    class Config:
        from_attributes = True
