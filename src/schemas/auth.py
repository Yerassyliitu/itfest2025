from pydantic import BaseModel, EmailStr

class EmailInput(BaseModel):
    email: EmailStr


class EmailCodeInput(BaseModel):
    email: EmailStr
    code: str