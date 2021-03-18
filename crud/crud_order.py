"""A crud method for order model"""
from crud.crud_base import CRUDBase
from models import Order
from schemas import Order as OrderSchema


class CRUDOrder(CRUDBase[Order, OrderSchema]):
    """Defined order crud method"""
    pass


order = CRUDOrder(Order)
