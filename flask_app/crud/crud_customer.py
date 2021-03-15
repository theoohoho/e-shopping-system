"""A crud method for customer model"""
from crud.crud_base import CRUDBase
from models import Customer
from schemas import Customer as CustomerSchema


class CRUDCustomer(CRUDBase[Customer, CustomerSchema]):
    """Defined customer crud method"""
    pass


customer = CRUDCustomer(Customer)
