from flask_restplus import Namespace, fields


class EmailDTO:
    api = Namespace('Email', description='Email related operations')
    email = api.model('Email', {
        'locationId': fields.String(required=True, description='The Email location id'),
        'nameEn': fields.String(required=True, description='Email name in french'),
        'nameFr': fields.String(required=True, description='Email name in english'),
        'email': fields.String(required=True, description='Email')
    })
    email_id = api.model('Email id', {
        'id': fields.Integer(required=True, description='The Email id'),
    })
