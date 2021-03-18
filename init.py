"""Init create table schema in database.
"""
from models import Base
from database import engine, get_db_session
from crud.crud_product import product as product_operation
from schemas import Product
import os
import json


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


if __name__ == "__main__":
    initial_database()
    with get_db_session() as db_session:
        insert_dummy_movie(db_session)
        db_session.commit()
