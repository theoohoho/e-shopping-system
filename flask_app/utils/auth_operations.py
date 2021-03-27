from flask import request
from jwt.exceptions import ExpiredSignatureError

from utils.jwt_operations import decode_jwt
from config import DEBUG_MODE
from functools import wraps


def user_token_verification(func):
    """Verify user token"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt(token) if token else dict()
            # not decide a place to store cart_id token yet, so hardcode it
            parsed_info = dict(
                user_id='tmp_user' if DEBUG_MODE else payload.get('user_id'),
                cart_id='tmp_cart'
            )
            return func(parsed_info, *args, **kwargs)
        except ExpiredSignatureError:
            print('Expired token, please re-login user')
        except Exception:
            raise
    return wrapper
