from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.types import VARCHAR, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(VARCHAR(50), primary_key=True)
    username = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False)

    order = relationship('Order', backref='user')


class UserLoginHistory(Base):
    __tablename__ = 'user_login_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(VARCHAR(50), nullable=False)
    login_time = Column(DateTime, nullable=False)
    login_status = Column(VARCHAR(10), nullable=False)
    ip_address = Column(VARCHAR(10), )


class Product(Base):
    __tablename__ = 'product'

    product_id = Column(VARCHAR(40), primary_key=True)
    product_name = Column(VARCHAR(255), nullable=False)
    product_type = Column(VARCHAR(10), )
    store_pcs = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, )
    release_date = Column(VARCHAR(10), )
    movie_runtime = Column(VARCHAR(10), )
    movie_score = Column(VARCHAR(3), )
    source_url = Column(String, )
    image_url = Column(String, )

    order_items = relationship('OrderItems', backref='product')


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(Integer, primary_key=True)
    type_name = Column(VARCHAR(10), nullable=False)


class Order(Base):
    __tablename__ = 'order'

    order_id = Column(VARCHAR(50), primary_key=True)
    user_id = Column(VARCHAR(50), ForeignKey('user.user_id'))
    total_price = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)

    order_items = relationship('OrderItems', backref='order')


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(VARCHAR(50), ForeignKey('order.order_id'), nullable=False, index=True)
    product_id = Column(VARCHAR(40), ForeignKey('product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(VARCHAR(50), nullable=False)
    product_id = Column(VARCHAR(40), nullable=False)
    product_qty = Column(Integer)


class UserFavoriteProduct(Base):
    __tablename__ = 'user_favorite_product'

    id = Column(Integer, primary_key=True)
    product_id = Column(VARCHAR(40))
    user_id = Column(VARCHAR(50))
