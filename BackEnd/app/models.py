from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)