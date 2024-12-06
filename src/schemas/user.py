from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserRead(BaseModel):
    id: int = Field(..., example=1, description="Unique identifier")
    email: Optional[EmailStr] = Field(..., description="Email address of the user")
