"""A crud method for Coupon model"""
from crud.crud_base import CRUDBase
from models import Coupon, CouponReceive
from schemas import Coupon as CouponSchema
from utils.exceptions import crud_exception_handler

from typing import List
from sqlalchemy.orm import Session


class CRUDCoupon(CRUDBase[Coupon, CouponSchema]):
    """Defined Coupon crud method"""

    @staticmethod
    def base_get_user_coupon(db: Session, user_id: str):
        return db.query(Coupon, CouponReceive).select_from(CouponReceive).join(
            Coupon, CouponReceive.coupon_id == Coupon.id
        ).filter(CouponReceive.user_id == user_id)


    @crud_exception_handler
    def get_user_coupon(self, db: Session, user_id: str, coupon_code: str):
        query_result = self.base_get_user_coupon(
            db=db, user_id=user_id
        ).filter(Coupon.coupon_code == coupon_code).first()
        if not query_result:
            return None, None
        return query_result

    @crud_exception_handler
    def find_enabled_user_coupon(self, db: Session, user_id: str, enabled: bool):
        query_result = self.base_get_user_coupon(
            db=db, user_id=user_id
        ).filter(CouponReceive.enabled == int(enabled)).first()
        if not query_result:
            return None, None
        return query_result

    @crud_exception_handler
    def get_all_user_coupon(self, db: Session, user_id: str, coupon_code: str) -> List:
        return self.base_get_user_coupon(
            db=db, user_id=user_id
        ).filter(Coupon.coupon_code == coupon_code).all()


coupon = CRUDCoupon(Coupon)
