from pydantic import BaseModel
import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_toke: str
    created_date: datetime.datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    user_id: int