from flask_restplus import Namespace, fields


class TelephoneDTO:
    api = Namespace('Telephone', description='Telephone related operations')
    telephone = api.model('telephone', {
        'locationId': fields.String(required=True, description='The telephone location id'),
        'nameEn': fields.String(required=True, description='telephone name in french'),
        'nameFr': fields.String(required=True, description='telephone name in english'),
        'telephone': fields.String(required=True, description='telephone number')
    })
    full_telephone = api.model('Full telephone', {
        'id': fields.Integer(required=True, description='The telephone id'),
        'locationId': fields.String(required=True, description='The telephone location id'),
        'nameEn': fields.String(required=True, description='telephone name in french'),
        'nameFr': fields.String(required=True, description='telephone name in english'),
        'telephone': fields.String(required=True, description='telephone number')
    })
    telephone_id = api.model('Telephone id', {
        'id': fields.Integer(required=True, description='The telephone id'),
    })
