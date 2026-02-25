from flask_restx import Namespace, fields


class EmailDTO:
    api = Namespace('Email', description='Email related operations')
    email = api.model('Email', {
        'locationId': fields.String(required=True, description='The Email location id'),
        'nameEn': fields.String(required=True, description='Email name in french'),
        'nameFr': fields.String(required=True, description='Email name in english'),
        'email': fields.String(required=True, description='Email'),
        'displayOrder': fields.Integer(required=False, description='Display Order'),
        'isCertipropane': fields.Boolean(required=False, description='Is Certipropane')
    })
    full_email = api.model('Full email', {
        'id': fields.Integer(required=True, description='The email id'),
        'locationId': fields.String(required=True, description='The Email location id'),
        'nameEn': fields.String(required=True, description='Email name in french'),
        'nameFr': fields.String(required=True, description='Email name in english'),
        'email': fields.String(required=True, description='Email'),
        'displayOrder': fields.Integer(required=False, description='Display Order'),
        'isCertipropane': fields.Boolean(required=False, description='Is Certipropane')
    })
    email_id = api.model('Email id', {
        'id': fields.Integer(required=True, description='The Email id'),
    })
