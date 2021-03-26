"""Defined jwt token operation
"""
import jwt
import time
from config import SECRET_KEY


def encode_jwt(payload: dict, expire_time: int) -> str:
    """Encode jwt token"""
    current_time = int(time.time())
    payload['iat'] = current_time
    payload['exp'] = current_time + expire_time
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_jwt(token: str) -> str:
    """Decode jwt token"""
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")
