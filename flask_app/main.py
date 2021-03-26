from flask_cors import CORS
from flask import Flask, jsonify, request, _app_ctx_stack

from sqlalchemy.orm import scoped_session
import uuid
import datetime

from database import SessionLocal
from crud.crud_product import product as product_operation
from crud.crud_order import order as order_operation
from crud.crud_cart_items import cart_items as cart_items_operation

from schemas import (
    Product as ProductSchema,
    Order as OrderSchema,
    CartItems as CartItemsSchema,
    OrderItems as OrderItemsSchema,
    ResponseOrderList,
    ResponseProductList,
    ResponseCartList
)

import config
from utils import helper

app = Flask(__name__)
app.config.update(JSON_AS_ASCII=False)
CORS(app)

# Handle SQLAlchemy with Flask app, to approach thread safe
# https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
app.session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# Aa a fake user for debug mode
fake_customer = {
    "user_id": 'fake_customer',
    "username": 'fake_customer',
    "token": helper.gen_user_token(user_id='fake_customer')
}

@app.route('/')
def hello_world():
    """api router"""
    return 'Hello, World!'


@app.route('/api/v1/admin/login', methods=["POST"])
def admin_login():
    """管理員登入"""
    print(request.json)
    return jsonify({
        "message": "Success"
    })


@app.route('/api/v1/admin/logout', methods=["POST"])
def admin_logout():
    """管理員登出"""
    print(request.json)
    return jsonify({
        "message": "Success"
    })


@app.route('/api/v1/admin/signup', methods=["POST"])
def admin_signup():
    """管理員註冊"""
    print(request.json)
    return jsonify({
        "message": "Success"
    })


@app.route('/api/v1/signup', methods=["POST"])
def user_signup():
    """註冊會員"""
    register_info = request.json

    return jsonify({
        "message": "Success"
    })


@app.route('/api/v1/login', methods=["POST"])
def user_login():
    """登入會員"""
    login_info = request.json
    username = login_info.get('username')
    password = login_info.get('password')

    # get fake customer for debug mode
    if config.DEBUG_MODE:
        username = fake_customer.get("user_id")
    return jsonify({
        "token": helper.gen_user_token(user_id=username),
        "message": "Success"
    })


@app.route('/api/v1/logout', methods=["POST"])
def user_logout():
    """登出會員"""
    print(request.json)
    return jsonify({
        "message": "Success"
    })


@app.route('/api/v1/product', methods=["GET"])
def get_product_list():
    """取得產品列表"""
    products = product_operation.get_all(app.session)
    query_result = [ProductSchema(**product.__dict__).dict() for product in products]
    resp = ResponseProductList(
        data=query_result,
        current_page=1,
        current_count=len(query_result),
        total_count=len(query_result)
    ).dict()
    return jsonify(resp)


@app.route('/api/v1/product/<string:product_id>', methods=["GET"])
def get_product(product_id):
    """取得產品資訊"""
    query_result = product_operation.get(app.session, {"product_id": product_id})
    resp = ProductSchema(**query_result.__dict__).dict()
    return jsonify(resp)


@app.route('/api/v1/cart', methods=["POST"])
def add_cart():
    """加入單項產品至購物車"""
    try:
        username = fake_customer.get("user_id") if config.DEBUG_MODE else None
        body = request.json
        product_id = body.get('product_id')
        product_qty = body.get('product_qty')
        if not product_qty or not product_id:
            raise Exception('Request body is empty, please check your request message')

        # check product quantity is valid
        product = product_operation.get(db=app.session, filter_dict={
            'product_id': product_id
        })
        if product_qty > product.store_pcs:
            raise Exception('Product haven\'t enough piece to buy')

        # create cart_items or update product quantity in cart_items
        cart_item = cart_items_operation.get(db=app.session, filter_dict={
            'product_id': product_id,
            'cart_id': username
        })
        if not cart_item:
            new_cart_item = CartItemsSchema(
                product_id=product_id,
                product_qty=product_qty,
                cart_id=username
            )
            cart_items_operation.create(db=app.session, obj_in=new_cart_item)
        else:
            cart_item.product_qty += product_qty
            if cart_item.product_qty > product.store_pcs:
                raise Exception('Exceeded product inventory quantity')
            app.session.commit()

        return jsonify({
            "message": "Success to add product into shopping cart, please check your shopping cart"
        })
    except Exception:
        raise


@app.route('/api/v1/cart', methods=["GET"])
def get_cart_list():
    """取得購物車內容"""
    try:
        query_result = []
        total_price = 0
        db_query = cart_items_operation.get_cart_item_with_product(app.session)

        for cart_item, product in db_query:
            product_total_price = cart_item.product_qty * product.price
            total_price += product_total_price
            query_result.append({
                "product_id": cart_item.product_id,
                "product_name": product.product_name,
                "product_qty": cart_item.product_qty,
                "product_total_price": product_total_price,
            })

        resp = ResponseCartList(
            data=query_result,
            total_price=total_price
        ).dict()

        # add cart token to target user shopping cart
        resp['cart_token'] = helper.gen_shopping_cart_token(fake_customer.get("user_id"))

        return jsonify(resp)
    except Exception:
        raise


@app.route('/api/v1/order', methods=["POST"])
def order():
    """結帳"""
    try:
        # assume decoded token can get user_id
        customer_id = 'tmp_test'
        total_price = 0
        order_id = str(uuid.uuid4())
        order_time = datetime.datetime.now()
        db_query = cart_items_operation.get_cart_item_with_product(db=app.session)

        # transfer each cart_item to be order_item
        order_items = []
        for cart_item, product in db_query:
            order_item_total_price = cart_item.product_qty * product.price
            total_price += order_item_total_price
            order_items.append(OrderItemsSchema(
                order_id=order_id,
                product_id=cart_item.product_id,
                quantity=cart_item.product_qty,
                price=order_item_total_price
            ))
            # after cart_item transfer to order_item, should deleted it
            app.session.delete(cart_item)
        order_operation.add_order_items(db=app.session, obj_in=order_items)

        # create order
        order_operation.create(db=app.session, obj_in=OrderSchema(
            order_id=order_id,
            customer_id=customer_id,
            total_price=total_price,
            order_time=order_time
        ))

        app.session.commit()

        return jsonify({
            "order_id": order_id,
            "order_date": str(order_time),
            "message": "Success"
        })
    except Exception:
        raise


@app.route('/api/v1/order', methods=["GET"])
def get_order_list():
    """取得訂單列表"""
    orders = order_operation.get_all(app.session)
    result = [OrderSchema(**order.__dict__).dict() for order in orders]
    output_format = {
        "data": [{
            "order_id": "",
            "order_amount": "",
            "order_date": ""
        }],
        "page": 1,
        "current_count": len(result),
        "total_count": len(result)
    }
    output_format['data'] = result
    return jsonify(output_format)


@app.route('/api/v1/product/<string:product_id>/favorite', methods=["POST"])
def tag_favorite(product_id):
    """加入產品至會員收藏"""
    print(request.json)
    return jsonify({
        "product_id": "",
        "message": "Success to add a new collect"
    })


@app.route('/api/v1/favorite', methods=["GET"])
def get_favorite_list():
    """會員收藏列表"""
    return jsonify({
        "data": [{
            "product_id": "",
            "product_name": "",
            "product_price": "",
            "product_type": "",
            "image_url": ""
        }],
        "page": 0,
        "current_count": 0,
        "total_count": 0
    })


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    """Handle each created session can close and remove properly, it will terminated local and remove session object"""
    app.session.remove()
