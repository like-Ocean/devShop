from flask import Blueprint, request, jsonify, make_response, Response
from webargs import flaskparser
from service import user_service
from decorators import login_required, role_required
from .fields import register_model, edit_model, logout_model, set_user_role_model, authorization_model

user_router = Blueprint('user', __name__)


@user_router.post('/user/registration')
def registration():
    data = flaskparser.parser.parse(register_model, request)
    user = user_service.registration(
        data['first_name'], data['surname'],
        data['phone'], data['email'], data['password']
    )
    return jsonify(user)


# мб нужно переписать
@user_router.post('/user/authorization')
def auth():
    data = flaskparser.parser.parse(authorization_model, request)
    result = user_service.authorization(data['email'], data['password'])
    if isinstance(result, dict):
        resp = make_response(jsonify(result))
        if 'ref_token' in result:
            resp.set_cookie('ref_token', result['ref_token'], httponly=True)
        return resp
    else:
        return jsonify({'error': result})


@user_router.get('/user/refresh')
def refresh():
    refresh_token = request.cookies.get('ref_token')
    if not refresh_token:
        return 'User is not authorized', 401

    new_access_token, new_ref_token = user_service.ref_tokens(refresh_token)
    response = make_response(jsonify(new_access_token))
    response.set_cookie('ref_token', new_ref_token)
    return response


@user_router.post('/user/logout')
@login_required
def logout():
    refresh_token = request.cookies.get('ref_token')
    res = make_response(refresh_token)
    res.delete_cookie('ref_token')
    data = flaskparser.parser.parse(logout_model, request)
    user = user_service.logout(data['user_id'])
    return jsonify(user)


@user_router.get('/users')
@login_required
@role_required('ADMIN')
def get_users():
    users = user_service.get_users()
    return jsonify(users)


@user_router.delete('/user/delete')
@login_required
@role_required('ADMIN')
def delete_user():
    data = flaskparser.parser.parse(logout_model, request)
    delete = user_service.delete_user(data['user_id'])
    return jsonify(delete)


@user_router.post('/user/edit')
@login_required
def edit_user():
    data = flaskparser.parser.parse(edit_model, request)
    user = user_service.edit_user(
        data['user_id'], data['first_name'], data['surname'],
        data['phone'], data['email'], data['password']
    )
    return jsonify(user)


@user_router.post('/user/set_user_role')
@login_required
@role_required('ADMIN')
def set_user_role():
    data = flaskparser.parser.parse(set_user_role_model, request)
    user = user_service.set_user_role(data['user_id'], data['role_id'])
    return jsonify(user)


@user_router.delete('/user/remove_user_role')
@login_required
@role_required('ADMIN')
def remove_user_role():
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_service.remove_user_role(data['user_id'], data['role_id'])
    return Response(status=204)


@user_router.get('/user/<user_id>')
def get_user(user_id):
    user = user_service.get_user(user_id)
    return jsonify(user)
