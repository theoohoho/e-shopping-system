"""Init create table schema in database.
"""
from models import Base
from database import engine, get_db_session
from crud.crud_product import product as product_operation
from crud.crud_coupon import coupon as coupon_operation
from crud.crud_user import user as user_operation
from schemas import Product, Coupon, User
from models import CouponReceive

import os
import json
import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def initial_database():
    Base.metadata.create_all(bind=engine)


def insert_dummy_movie(db_session):
    """
    Insert dummy movie data into database

    1. check dummy file
    2. insert dummy movie data
    """
    print('Insert dummy movie data....')
    dummy_file_path = os.path.join(BASE_DIR, 'dummy', 'dummy_movie.json')
    if not os.path.isfile(dummy_file_path):
        raise Exception(f'dummy file not found: {dummy_file_path}')

    with open(dummy_file_path) as conetnt:
        raw_content = conetnt.read()
        json_content = json.loads(raw_content)
        dummy_movie_list = [Product(**dummy_movie) for dummy_movie in json_content]

    product_operation.add_all(db_session, dummy_movie_list)


def insert_test_user(db_session):
    from utils.helper import hash_password
    test_user = [User(
        user_id='tmp_user',
        username='tmp_user',
        password=hash_password('tmp_user'),
        email='tmp_user@gmail.com'
    )]
    user_operation.add_all(db=db_session, obj_in=test_user)


def insert_dummy_coupon(db_session):
    dummy_coupons = [Coupon(
        coupon_code='test_code',
        coupon_name='測試折扣券',
        coupon_qty=99999999,
        discount='0.7',
        begin_time=datetime.datetime.now(),
        end_time=datetime.datetime.now() + datetime.timedelta(days=9999),
        create_time=datetime.datetime.now(),
        status=0,
        description='測試折扣專用',
    )]
    coupon_operation.add_all(db=db_session, obj_in=dummy_coupons)


def insert_user_coupon(db_session):
    db_session.add(
        CouponReceive(
            user_id='tmp_user',
            coupon_id=1,
            receive_time=datetime.datetime.now(),
            status=1,
            enabled=1,
        ))


if __name__ == "__main__":
    initial_database()
    with get_db_session() as db_session:
        insert_dummy_movie(db_session)
        insert_dummy_coupon(db_session)
        insert_test_user(db_session)
        insert_user_coupon(db_session)
        db_session.commit()
