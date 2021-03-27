"""A crud method for cart_items model"""
from typing import List
from sqlalchemy.orm import Session

from crud.crud_base import CRUDBase
from models import CartItems, Product
from schemas import CartItems as CartItemsSchema

from utils.exceptions import crud_exception_handler


class CRUDCartItems(CRUDBase[CartItems, CartItemsSchema]):
    """Defined cart_items crud method"""

    @staticmethod
    def get_cart_item_base(db: Session):
        """Base sql statement to get cart items"""
        return db.query(CartItems, Product).select_from(CartItems).join(Product, CartItems.product_id == Product.product_id)

    @crud_exception_handler
    def get_cart_item_with_product(self, db: Session, cart_id: str) -> List:
        """Get cart items"""
        return self.get_cart_item_base(db).filter(CartItems.cart_id == cart_id).all()


cart_items = CRUDCartItems(CartItems)
