from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('User', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })
    user_change_password = api.model('user_change_password', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'confirm_password': fields.String(required=True, description='user confirm password'),
    })
