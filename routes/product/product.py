from flask import Blueprint, request, jsonify, make_response, Response
from webargs import flaskparser
from service import product_service
from decorators import login_required, role_required
from .fields import add_category_model, remove_category_model, add_product_model, \
    change_product_model, remove_product_model, upload_file_model, remove_file_model

product_router = Blueprint('product', __name__)


@product_router.post('/category/add')
@role_required('ADMIN')
@login_required
def add_category():
    data = flaskparser.parser.parse(add_category_model, request)
    category = product_service.add_category(data['name'], data['slug'])
    return jsonify(category)


@product_router.delete('/category/remove')
@role_required('ADMIN')
@login_required
def remove_category():
    data = flaskparser.parser.parse(remove_category_model, request)
    category = product_service.remove_category(data['category_id'])
    return jsonify(category)


@product_router.get('/categories/')
def get_categories():
    category = product_service.get_categories()
    return jsonify(category)


@product_router.get('/category/<category_id>/')
def get_category(category_id):
    category = product_service.get_category(category_id)
    return jsonify(category)


@product_router.post('/product/add')
@login_required
@role_required('ADMIN')
def add_product():
    data = flaskparser.parser.parse(add_product_model, request)
    product = product_service.add_product(
        data['category_id'], data['name'], data['description'],
        data['price'], data['discount'], data['total_count']
    )
    return jsonify(product)


@product_router.post('/product/change')
@login_required
@role_required('ADMIN')
def change_product():
    data = flaskparser.parser.parse(change_product_model, request)
    product = product_service.change_product(
        data['product_id'], data['category_id'], data['name'], data['description'],
        data['price'], data['discount'], data['total_count']
    )
    return jsonify(product)


@product_router.get('/products/')
def get_products():
    products = product_service.get_products()
    return jsonify(products)


@product_router.get('/product/<product_id>/')
def get_product(product_id):
    product = product_service.get_product(product_id)
    return jsonify(product)


@product_router.delete('/product/remove')
@role_required('ADMIN')
@login_required
def remove_product():
    data = flaskparser.parser.parse(remove_product_model, request)
    product = product_service.remove_product(data['product_id'])
    return jsonify(product)


@product_router.get('/product/product/<category_id>/')
def get_in_category_products(category_id):
    products = product_service.get_in_category_products(category_id)
    return jsonify(products)


@product_router.post('/product/file/upload')
@role_required('ADMIN')
@login_required
def upload_file_product():
    data = flaskparser.parser.parse(upload_file_model, request,  location='form')
    file = request.files['file']
    img = product_service.add_product_img(data['product_id'], file)
    return jsonify(img)


@product_router.delete('/product/file/remove')
@role_required('ADMIN')
@login_required
def remove_file_product():
    data = flaskparser.parser.parse(remove_file_model, request)
    file = product_service.remove_product_img(data['img_id'])
    return jsonify(file)
