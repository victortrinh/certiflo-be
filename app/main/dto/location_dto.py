from flask_restplus import Namespace, fields


class LocationDTO:
    api = Namespace('Location', description='Location related operations')
    location = api.model('location', {
        'nameEn': fields.String(required=True, description='location name in french'),
        'nameFr': fields.String(required=True, description='location name in english'),
        'address': fields.String(required=True, description='location address')
    })
    location_id = api.model('Location id', {
        'id': fields.Integer(required=True, description='The location id'),
    })
