from webargs import fields

make_order_model = {
    'user_id': fields.Integer(required=True),
    'address': fields.String(required=True),
    'products_id': fields.List(fields.Nested({'product_id': fields.Integer(required=True), 'count': fields.Integer(required=True)}))
}

delete_order_model = {
    'order_id': fields.Integer(required=True)
}


edit_order_model = {
    'user_id': fields.Integer(required=True),
    'order_id': fields.Integer(required=True),
    'address': fields.String(required=False),
    'products_id': fields.List(fields.Nested({'product_id': fields.Integer(required=True), 'count': fields.Integer(required=True)}))
}