import jwt
import os
import dotenv
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

dotenv.load_dotenv()


def decode_jwt(jwt_token: str):
    try:
        payload = jwt.decode(jwt_token, os.getenv("JWT_SECRET_KEY"), "HS256")

        return payload
    except InvalidTokenError:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(token)
            print(payload)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


jwt_bearer = JWTBearer()
