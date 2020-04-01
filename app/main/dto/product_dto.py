from flask_restplus import Namespace, fields


class ProductDTO:
    api = Namespace('Product', description='Product related operations')
    product = api.model('Product', {
        'nameEn': fields.String(required=True, description='Product name in french'),
        'nameFr': fields.String(required=True, description='Product name in english'),
        'image': fields.String(required=True, description='Image'),
        'descriptionEn': fields.String(required=True, description='Product description in french'),
        'descriptionFr': fields.String(required=True, description='Product name in english'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    full_product = api.model('Full product', {
        'id': fields.Integer(required=True, description='The product id'),
        'nameEn': fields.String(required=True, description='Product name in french'),
        'nameFr': fields.String(required=True, description='Product name in english'),
        'image': fields.String(required=True, description='Image'),
        'descriptionEn': fields.String(required=True, description='Product description in french'),
        'descriptionFr': fields.String(required=True, description='Product name in english'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    product_id = api.model('Product id', {
        'id': fields.Integer(required=True, description='The Product id'),
    })
