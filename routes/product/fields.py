from webargs import fields

add_category_model = {
    'name': fields.String(required=True),
    'slug': fields.String(required=True)
}

remove_category_model = {
    'category_id': fields.Integer(required=True)
}

add_product_model = {
    'category_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'discount': fields.Integer(required=False),
    'total_count': fields.Integer(required=True)
}

change_product_model = {
    'product_id': fields.Integer(required=True),
    'category_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'discount': fields.Integer(required=False),
    'total_count': fields.Integer(required=True)
}

remove_product_model = {
    'product_id': fields.Integer(required=True)
}

upload_file_model = {
    'product_id': fields.Integer(required=True)
}

remove_file_model = {
    'img_id': fields.Integer(required=True)
}