"""A crud method for order model"""
from typing import List
from sqlalchemy.orm import Session

from crud.crud_base import CRUDBase
from models import Order, OrderItems
from schemas import Order as OrderSchema, OrderItems as OrderItemsSchema

from utils.exceptions import crud_exception_handler


class CRUDOrder(CRUDBase[Order, OrderSchema]):
    """Defined order crud method"""

    @crud_exception_handler
    def add_order_items(self, db: Session, obj_in: List[OrderItemsSchema]) -> None:
        db_obj = [OrderItems(**obj.dict()) for obj in obj_in]
        print(db_obj)
        db.add_all(db_obj)


order = CRUDOrder(Order)
