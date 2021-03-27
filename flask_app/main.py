from flask_cors import CORS
from flask import Flask, jsonify, request, _app_ctx_stack

from sqlalchemy.orm import scoped_session
import uuid
import datetime

from database import SessionLocal
from crud.crud_product import product as product_operation
from crud.crud_order import order as order_operation
from crud.crud_cart_items import cart_items as cart_items_operation
from crud.crud_user import user as user_operation

from schemas import (
    Product as ProductSchema,
    Order as OrderSchema,
    CartItems as CartItemsSchema,
    OrderItems as OrderItemsSchema,
    User as UserSchema,
    UserLoginHistory as LoginHistorySchema,
    UserFavoriteProduct as UserFavoriteProductSchema,
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
fake_user = {
    "user_id": 'fake_user',
    "username": 'fake_user',
    "token": helper.gen_user_token(user_id='fake_user')
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
    username = register_info.get('username')
    password = register_info.get('password')
    email = register_info.get('email')

    # verify user existence
    if user_operation.get(db=app.session, filter_dict={"username": username}):
        raise Exception('User exists, please naming other username')

    # create user
    hashed_password = helper.hash_password(password)
    user = UserSchema(
        user_id=str(uuid.uuid4()),
        username=username,
        password=hashed_password,
        email=email,
    )
    user_operation.create(db=app.session, obj_in=user)

    return jsonify({
        "message": f"Success to register user: {username}"
    })


@app.route('/api/v1/login', methods=["POST"])
def user_login():
    """登入會員"""
    login_info = request.json
    username = login_info.get('username')
    password = login_info.get('password')
    resp = {
        "token": "",
        "message": f"Login success: {username}"
    }

    # get fake user for debug mode
    if config.DEBUG_MODE:
        resp['token'] = fake_user.get("token")
        return jsonify(resp)

    # verify user existence and user password
    user = user_operation.get(db=app.session, filter_dict={"username": username})
    if not user:
        raise Exception('User not found, please register first')
    if not helper.verify_password(password=password, hashed_password=user.hashed_password):
        raise Exception('Invalid passsword, please insert right password')

    # record user login history
    login_history = LoginHistorySchema(
        user_id=user.user_id,
        login_time=datetime.datetime.now(),
        login_status='login',
        ip_address=request.remote_addr,
    )
    user_operation.create_login_history(db=app.session, obj_in=login_history)
    resp['token'] = helper.gen_user_token(user_id=username)
    return jsonify(resp)


@app.route('/api/v1/logout', methods=["POST"])
def user_logout():
    """登出會員"""
    return jsonify({
        "username": '',
        "timestamp": datetime.datetime.now(),
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
        username = fake_user.get("user_id") if config.DEBUG_MODE else None
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
        resp['cart_token'] = helper.gen_shopping_cart_token(fake_user.get("user_id"))

        return jsonify(resp)
    except Exception:
        raise


@app.route('/api/v1/order', methods=["POST"])
def order():
    """結帳"""
    try:
        # assume decoded token can get user_id
        user_id = 'tmp_test'
        total_price = 0
        order_id = str(uuid.uuid4())
        order_date = datetime.datetime.now()
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
            # deduct order quantity
            product.store_pcs -= cart_item.product_qty

        order_operation.add_order_items(db=app.session, obj_in=order_items)

        # create order
        order_operation.create(db=app.session, obj_in=OrderSchema(
            order_id=order_id,
            user_id=user_id,
            total_price=total_price,
            order_date=order_date
        ))

        app.session.commit()

        return jsonify({
            "order_id": order_id,
            "order_date": str(order_date),
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
        "current_page": 1,
        "current_count": len(result),
        "total_count": len(result)
    }
    output_format['data'] = result
    return jsonify(output_format)


@app.route('/api/v1/favorite', methods=["POST"])
def tag_favorite():
    """加入產品至會員收藏"""
    user_id = fake_user.get("user_id") if config.DEBUG_MODE else None
    favorite_info = request.json
    product_id = favorite_info.get("product_id")

    # verify product existence in favorite collection
    if user_operation.get_one_user_favorite(db=app.session, user_id=user_id, product_id=product_id):
        raise Exception(f"Already add product {product_id} into favorite collection")

    new_favorite = UserFavoriteProductSchema(user_id=user_id, product_id=product_id)
    user_operation.create_user_favorite(db=app.session, obj_in=new_favorite)
    return jsonify({
        "message": f"Success to add a new favorite: {product_id}"
    })


@app.route('/api/v1/favorite', methods=["DELETE"])
def delete_favorite():
    """移除會員單一收藏"""
    user_id = fake_user.get("user_id") if config.DEBUG_MODE else None
    favorite_info = request.json
    product_id = favorite_info.get("product_id")
    user_operation.remove_user_favorite(db=app.session, filter_dict=dict(user_id=user_id, product_id=product_id))
    return jsonify({
        "message": f"Delete a favorite: {product_id}"
    })


@app.route('/api/v1/favorite', methods=["GET"])
def get_favorite_list():
    """會員收藏列表"""
    user_id = fake_user.get("user_id") if config.DEBUG_MODE else None
    user_favorites = user_operation.get_all_user_favorites(db=app.session, user_id=user_id)
    query_result = [ProductSchema(**product.__dict__).dict() for product in user_favorites]
    return jsonify({ 
        "data": query_result,
        "current_page": 1,
        "current_count": len(query_result),
        "total_count": len(query_result)
    })


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    """Handle each created session can close and remove properly, it will terminated local and remove session object"""
    app.session.remove()
