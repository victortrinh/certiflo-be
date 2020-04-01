from flask_restplus import Namespace, fields


class GalleryDTO:
    api = Namespace(
        'Gallery', description='Gallery related operations')
    gallery = api.model('Gallery', {
        'company': fields.String(required=True, description='Gallery company'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    full_gallery = api.model('Full gallery', {
        'id': fields.Integer(required=True, description='The gallery id'),
        'company': fields.String(required=True, description='Gallery company'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    gallery_id = api.model('Gallery id', {
        'id': fields.Integer(required=True, description='The Gallery id')
    })
