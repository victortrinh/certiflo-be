from flask_restplus import Namespace, fields


class ManufacturerImageDTO:
    api = Namespace('ManufacturerImage',
                    description='ManufacturerImage related operations')
    manufacturerImage = api.model('Manufacturer image', {
        'manufacturerId': fields.Integer(required=True, description='Manufacturer id'),
        'image': fields.String(required=True, description='image'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    manufacturerImageId = api.model('Manufacturer image id', {
        'id': fields.Integer(required=True, description='Manufacturer image id')
    })
