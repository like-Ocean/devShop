import os
from functools import wraps
import jwt
from flask import request, jsonify


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'no authorization token provided'}), 401
        try:
            token = auth_header.split(' ')[1]
            KEY = os.environ.get('SECRET_KEY')
            jwt.decode(token, KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return jsonify({'error': 'invalid authorization token'}), 401

        return func(*args, **kwargs)

    return decorated_function
