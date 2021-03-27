from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime


class User(BaseModel):
    user_id: str
    username: str
    password: str
    email: str


class UserLoginHistory(BaseModel):
    user_id: str
    login_time: datetime
    login_status: str
    ip_address: str


class UserFavoriteProduct(BaseModel):
    product_id: str
    user_id: str


class Product(BaseModel):
    product_id: str
    product_name: str
    product_type: Optional[str]
    store_pcs: int = 0
    price: int = 0
    description: Optional[str]
    release_date: Optional[str]
    movie_runtime: Optional[str]
    movie_score: Optional[str]
    image_url: Optional[str]
    source_url: Optional[str]


class ProductType(BaseModel):
    id: int
    type_name: str


class Order(BaseModel):
    order_id: str
    user_id: str
    total_price: int
    order_date: datetime


class OrderItems(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    price: int


class CartItems(BaseModel):
    cart_id: str
    product_id: str
    product_qty: int


# Defined response pydantic model
class BasePagnation(BaseModel):
    data: List[Any]
    current_page: int = 1
    current_count: int = 0
    total_count: int = 0


class ResponseProductList(BasePagnation):
    data: List[Product]


class ResponseOrderList(BasePagnation):
    data: List[Order]


class ResponseCartList(BaseModel):
    """Cart list response format

    expected data format as below:
    {
        data: [{
            product_id: ,
            product_name: ,
            product_qty: 0,
            product_price: ,
        }],
        total: 0
    }
    """
    data: List[dict]
    total_price: int
