from flask_restplus import Namespace, fields


class TankerTypeDTO:
    api = Namespace('TankerType', description='TankerType related operations')
    tankerType = api.model('TankerType', {
        'nameEn': fields.String(required=True, description='TankerType name in french'),
        'nameFr': fields.String(required=True, description='TankerType name in english'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    full_tankerType = api.model('Full tankerType', {
        'id': fields.Integer(required=True, description='The tankerType id'),
        'nameEn': fields.String(required=True, description='TankerType name in french'),
        'nameFr': fields.String(required=True, description='TankerType name in english'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    tankerType_id = api.model('TankerType id', {
        'id': fields.Integer(required=True, description='The TankerType id'),
    })
