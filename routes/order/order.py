from flask import Blueprint, request, jsonify, make_response, Response
from webargs import flaskparser
from service import order_service
from decorators import login_required
from .fields import make_order_model


order_router = Blueprint('order', __name__)


@order_router.post('/order/create')
@login_required
def make_order():
    data = flaskparser.parser.parse(make_order_model, request)
    order = order_service.make_order(data['user_id'], data['address'], data['products_id'])
    return jsonify(order)


