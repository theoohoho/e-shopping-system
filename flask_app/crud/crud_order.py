"""A crud method for order model"""
from typing import List
from sqlalchemy.orm import Session

from crud.crud_base import CRUDBase
from models import Order, OrderItems, Product, Coupon
from schemas import Order as OrderSchema, OrderItems as OrderItemsSchema

from utils.exceptions import crud_exception_handler


class CRUDOrder(CRUDBase[Order, OrderSchema]):
    """Defined order crud method"""

    @crud_exception_handler
    def add_order_items(self, db: Session, obj_in: List[OrderItemsSchema]) -> None:
        db_obj = [OrderItems(**obj.dict()) for obj in obj_in]
        print(db_obj)
        db.add_all(db_obj)


    @crud_exception_handler
    def get_order_info(self, db: Session, order_id: str):
        return db.query(
            Order, Coupon.coupon_name, Coupon.discount, OrderItems, Product.product_name, Product.image_url
        ).select_from(Order).join(
            Coupon, Coupon.coupon_code == Order.coupon_code
        ).join(
            OrderItems, Order.order_id == OrderItems.order_id
        ).join(
            Product, Product.product_id == OrderItems.product_id
        ).all()


order = CRUDOrder(Order)
