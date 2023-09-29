from webargs import fields

register_model = {
    'first_name': fields.String(required=True),
    'surname': fields.String(required=True),
    'phone': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
}

edit_model = {
    'user_id': fields.Integer(required=True),
    'first_name': fields.String(required=True),
    'surname': fields.String(required=True),
    'phone': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
}

logout_model = {
    'user_id': fields.Integer(required=True)
}

set_user_role_model = {
    'user_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True),
}

authorization_model = {
    'email': fields.String(required=False),
    'password': fields.String(required=False)
}