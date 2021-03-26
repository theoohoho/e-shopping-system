from utils import jwt_operations
import bcrypt


def gen_user_token(user_id: str) -> str:
    """Encode user token."""
    # set expire time for 10 minute
    payload = {
        "user_id": user_id
    }
    return jwt_operations.encode_jwt(payload, expire_time=(10 * 60))


def gen_shopping_cart_token(cart_id: str) -> str:
    """Generate token for shopping cart"""
    # set expire time for a day
    payload = {
        'cart_id': cart_id
    }
    return jwt_operations.encode_jwt(payload, expire_time=(60*60*24))


def hash_password(password: str) -> str:
    """Hash password by bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
