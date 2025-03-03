from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    username: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True 