import os
import requests
import dotenv
import jwt
from typing import Union, Any
import bcrypt
from datetime import datetime, timedelta
from fastapi import FastAPI
import pandas as pd

dotenv.load_dotenv()

app = FastAPI()

def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt(12))

def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(plain_pass, hashed_pass)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRY_MIN")))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY", "HS256"))
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRY_MIN")))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_REFRESH_SECRET_KEY"), 'HS256')
    return encoded_jwt