import os
from functools import wraps
from flask import request
from models import UserRole, Role
import jwt


def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    return 'token is not provided', 401
                token = token.split(' ')[1]
                payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
                user_id = payload['user_id']
                user_role = UserRole.select().join(Role).where(UserRole.user == user_id, Role.slug == role)
                if not user_role:
                    return 'You do not have an administrator role', 403

            except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
                return 'token expired or invalid', 401

            return func(*args, **kwargs)
        return decorated_function
    return decorator
