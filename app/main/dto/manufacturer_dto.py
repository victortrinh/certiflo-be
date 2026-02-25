from flask_restx import Namespace, fields


class ManufacturerDTO:
    api = Namespace(
        'Manufacturer', description='Manufacturer related operations')
    manufacturer = api.model('Manufacturer', {
        'nameEn': fields.String(required=True, description='name in english'),
        'nameFr': fields.String(required=True, description='name in french'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    manufacturer_id = api.model('Manufacturer id', {
        'id': fields.Integer(required=True, description='Manufacturer id')
    })
