from flask import Blueprint, request, jsonify
from webargs import flaskparser
from service import order_service
from decorators import login_required
from .fields import make_order_model, delete_order_model, edit_order_model


order_router = Blueprint('order', __name__)


@order_router.post('/order/create')
@login_required
def make_order():
    data = flaskparser.parser.parse(make_order_model, request)
    order = order_service.make_order(data['user_id'], data['address'], data['products_id'])
    return jsonify(order)


@order_router.get('/order/<order_id>/')
@login_required
def get_order_info(order_id):
    order = order_service.get_order_info(order_id)
    return jsonify(order)


@order_router.get('/orders/')
@login_required
def get_orders():
    order = order_service.get_orders_info()
    return jsonify(order)


@order_router.delete('/order/delete')
@login_required
def delete_order():
    data = flaskparser.parser.parse(delete_order_model, request)
    order = order_service.delete_order(data['order_id'])
    return jsonify(order)


@order_router.post('/order/edit')
@login_required
def edit_order():
    data = flaskparser.parser.parse(edit_order_model, request)
    order = order_service.change_order(
        data['user_id'], data['order_id'],
        data['address'], data['products_id']
    )
    return jsonify(order)


