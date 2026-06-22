from pydantic import BaseModel , Field
from typing import Optional
from datetime import datetime

class CreateTodo(BaseModel):
    content:str = Field(..., max_length=500 , min_length=5)
    is_completed:bool = False

class TodoResponse(BaseModel):
    id: int
    content: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True