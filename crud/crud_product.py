"""A crud method for product model"""
from crud.crud_base import CRUDBase
from models import Product
from schemas import Product as ProductSchema


class CRUDProduct(CRUDBase[Product, ProductSchema]):
    """Defined product crud method"""
    pass


product = CRUDProduct(Product)
