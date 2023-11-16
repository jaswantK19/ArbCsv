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
class UpdatedCSV(BaseModel):
    data: str  # Assuming the updated CSV data will be sent as a string

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    user_id: int