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
    status: bool
    created_date: datetime.datetime