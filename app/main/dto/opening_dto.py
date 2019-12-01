from flask_restplus import Namespace, fields


class OpeningDTO:
    api = Namespace('Opening', description='Opening related operations')
    opening = api.model('Opening', {
        'locationId': fields.String(required=True, description='The Opening location id'),
        'nameEn': fields.String(required=True, description='Opening name in french'),
        'nameFr': fields.String(required=True, description='Opening name in english'),
        'opening': fields.String(required=True, description='Opening'),
        'closing': fields.String(required=True, description='Closing')
    })
    full_opening = api.model('Full opening', {
        'id': fields.Integer(required=True, description='The telephone id'),
        'locationId': fields.String(required=True, description='The Opening location id'),
        'nameEn': fields.String(required=True, description='Opening name in french'),
        'nameFr': fields.String(required=True, description='Opening name in english'),
        'opening': fields.String(required=True, description='Opening'),
        'closing': fields.String(required=True, description='Closing')
    })
    opening_id = api.model('Opening id', {
        'id': fields.Integer(required=True, description='The Opening id'),
    })
