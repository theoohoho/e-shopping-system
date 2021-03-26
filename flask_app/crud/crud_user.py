"""A crud method for user model"""
from sqlalchemy.orm import Session

from crud.crud_base import CRUDBase
from models import User, UserLoginHistory
from schemas import User as UserSchema, UserLoginHistory as LoginHistorySchema

from utils.exceptions import crud_exception_handler


class CRUDUser(CRUDBase[User, UserSchema]):
    """Defined User crud method"""

    def create_login_history(self, db: Session, obj_in: LoginHistorySchema):
        """Create user login history"""
        created_obj = UserLoginHistory(**obj_in.dict())
        db.add(created_obj)
        db.commit()
        db.refresh(created_obj)
        return created_obj


user = CRUDUser(User)
