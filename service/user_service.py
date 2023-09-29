import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, JWT, Role, UserRole
import os

KEY = os.environ.get('SECRET_KEY')


def gen_token(user_id: int):
    access_token_data = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_data, KEY, algorithm='HS256')
    ref_token_data = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
        'iat': datetime.datetime.utcnow(),
    }
    ref_token = jwt.encode(ref_token_data, KEY, algorithm='HS256')
    return access_token, ref_token


def ref_tokens(refresh_token):
    try:
        payload = jwt.decode(refresh_token, KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        new_access_token, new_ref_token = gen_token(user_id)
        new_jwt = JWT(
            user=user_id,
            token=new_access_token,
            ref_token=new_ref_token
        )
        new_jwt.save()
        return new_access_token, new_ref_token
    except jwt.ExpiredSignatureError:
        return 'Refresh token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'


def registration(first_name: str, surname: str, phone: str, email: str, password: str):
    if User.select().where(User.email == email).exists():
        return 'email already exist'
    password_hash = generate_password_hash(password)
    user = User(
        first_name=first_name,
        surname=surname,
        phone=phone,
        email=email,
        password=password_hash
    )
    user.save()
    return user.get_dto()


def edit_user(user_id: int, first_name: str, surname: str, phone: str, email: str, password: str):
    user = User.get_or_none(id=user_id)
    if not user:
        return 'User not found'
    user.first_name = first_name
    user.surname = surname
    user.phone = phone
    user.email = email
    user.password = generate_password_hash(password)
    user.save()
    return user.get_dto()


def authorization(email: str, password: str):
    user = User.get_or_none(User.email == email)
    if not user or not check_password_hash(user.password, password):
        return 'Wrong email or password'

    access_token, ref_token = gen_token(user.id)
    jwts = JWT(
        user=user.id,
        token=access_token,
        ref_token=ref_token
    )
    jwts.save()
    return {**user.get_dto(), 'access_token': access_token, 'ref_token': ref_token}


def logout(user_id: int):
    user = User.get_or_none(id=user_id)
    if not user:
        return 'User not found'
    drop = JWT.delete().where(JWT.user_id == user_id)
    drop.execute()
    return 'Logged out', 200


def get_users():
    users = User.select()
    return [user.get_dto() for user in users]


def delete_user(user_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return 'User not found', 401
    drop = User.delete().where(User.id == user_id)
    drop.execute()
    return 200


def set_user_role(user_id: int, role_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return 'User not found', 401

    role = Role.get_or_none(Role.id == role_id)
    if not role:
        return 'Role not found'

    user_role = UserRole.get_or_none(user=user, role=role)
    if user_role:
        return 'User has already been assigned to this role'

    user_role = UserRole(user=user, role=role)
    user_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.first_name} {user.surname}',
        'role': role.get_dto()
    }


def remove_user_role(user_id: int, role_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return 'User not found', 401

    role = Role.get_or_none(Role.id == role_id)
    if not role:
        return 'Role not found'

    user_role = UserRole.get_or_none(user=user, role=role)
    if not user_role:
        return 'User is not assigned to this role'

    UserRole.delete().where(UserRole.id == user_role).execute()


def get_user(user_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return 'User not found', 401
    return user.get_dto()
