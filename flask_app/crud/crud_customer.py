"""A crud method for customer model"""
from sqlalchemy.orm import Session

from crud.crud_base import CRUDBase
from models import Customer, CustomerLoginHistory
from schemas import Customer as CustomerSchema, CustomerLoginHistory as LoginHistorySchema

from utils.exceptions import crud_exception_handler


class CRUDCustomer(CRUDBase[Customer, CustomerSchema]):
    """Defined customer crud method"""

    def create_login_history(self, db: Session, obj_in: LoginHistorySchema):
        """Create user login history"""
        created_obj = CustomerLoginHistory(**obj_in.dict())
        db.add(created_obj)
        db.commit()
        db.refresh(created_obj)
        return created_obj


customer = CRUDCustomer(Customer)
