from pydantic import BaseModel, Field
from typing import Optional, Any, List, Union
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
    coupon_code: str


class OrderItems(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    price: int


class CartItems(BaseModel):
    cart_id: str
    product_id: str
    product_qty: int


class Coupon(BaseModel):
    coupon_code: str
    coupon_name: str
    coupon_qty: int
    discount: str
    begin_time: datetime
    end_time: datetime
    create_time: datetime
    status: int
    description: str

# Defined api response pydantic model
class BasePagnation(BaseModel):
    data: List[Any]
    current_page: int = 1
    current_count: int = 0
    total_count: int = 0


class ResponseProductList(BasePagnation):
    data: List[Product]


class ResponseOrderList(BasePagnation):
    data: List[Order]


class RespCouponInfo(BaseModel):
    """The coupon info in the response of shopping cart list"""
    coupon_code: str
    coupon_name: str
    discount: float


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
    coupon_info: Union[RespCouponInfo, dict]
    total_price: int
    discount_price: int
    final_price: int


class CartItemDetail(BaseModel):
    """The response of the cart item detail of list"""
    product_id: str
    product_name: str
    product_type: str
    product_qty: int
    product_price: int
    product_total_price: int
    product_discount_price: int
    product_final_price: int
    image_url: str


class RespOrderItems(OrderItems):
    """The response of order items"""
    product_name: str
    image_url: str


class RespOrderInfo(BaseModel):
    """ The response of order infomation"""
    order_info: Order
    order_items: List[RespOrderItems]
    coupon_info: Union[RespCouponInfo, dict]
