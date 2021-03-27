"""A crud method for user model"""
from sqlalchemy.orm import Session
from typing import Dict, List

from crud.crud_base import CRUDBase
from models import User, UserLoginHistory, UserFavoriteProduct, Product
from schemas import User as UserSchema, UserLoginHistory as LoginHistorySchema, UserFavoriteProduct as UserFavoriteProductSchema

from utils.exceptions import crud_exception_handler


class CRUDUser(CRUDBase[User, UserSchema]):
    """Defined User crud method"""

    @crud_exception_handler
    def create_login_history(self, db: Session, obj_in: LoginHistorySchema):
        """Create user login history"""
        created_obj = UserLoginHistory(**obj_in.dict())
        db.add(created_obj)
        db.commit()
        db.refresh(created_obj)
        return created_obj

    @staticmethod
    def get_user_favorite_base(db: Session):
        """Base sql statement to get user favorite"""
        return db.query(Product).select_from(UserFavoriteProduct).join(
            Product, UserFavoriteProduct.product_id == Product.product_id
        )

    @crud_exception_handler
    def get_all_user_favorites(self, db: Session, user_id: str) -> List[Product]:
        """Get all of favorite product"""
        base_statement = self.get_user_favorite_base(db)
        return base_statement.filter(UserFavoriteProduct.user_id == user_id).all()

    @crud_exception_handler
    def get_one_user_favorite(self, db: Session, user_id: str, product_id: str) -> List[Product]:
        """Get a user favorite product"""
        base_statement = self.get_user_favorite_base(db)
        return base_statement.filter(
            UserFavoriteProduct.user_id == user_id,
            UserFavoriteProduct.product_id == product_id
        ).first()

    @crud_exception_handler
    def create_user_favorite(self, db: Session, obj_in: UserFavoriteProductSchema):
        """Create user favorite"""
        created_obj = UserFavoriteProduct(**obj_in.dict())
        db.add(created_obj)
        db.commit()
        db.refresh(created_obj)
        return created_obj

    @crud_exception_handler
    def remove_user_favorite(self,  db: Session, filter_dict: Dict = {}) -> UserFavoriteProduct:
        """Remove user favorite product"""
        db_obj = db.query(UserFavoriteProduct).filter_by(**filter_dict).first()
        db.delete(db_obj)
        db.commit()
        return db_obj


user = CRUDUser(User)
