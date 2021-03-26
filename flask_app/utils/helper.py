from utils import jwt_operations


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
