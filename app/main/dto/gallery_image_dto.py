from flask_restx import Namespace, fields


class GalleryImageDTO:
    api = Namespace(
        'GalleryImage', description='GalleryImage related operations')
    galleryImage = api.model('GalleryImage', {
        'image': fields.String(required=True, description='Gallery Image'),
        'galleryId': fields.String(required=True, description='Gallery Id'),
        'displayOrder': fields.Integer(required=False, description='Display Order'),
        'isCertipropane': fields.Boolean(required=False, description='Is Certipropane')
    })
    full_galleryImage = api.model('Full galleryImage', {
        'id': fields.Integer(required=True, description='The galleryImage id'),
        'image': fields.String(required=True, description='Gallery Image'),
        'galleryId': fields.String(required=True, description='Gallery Id'),
        'displayOrder': fields.Integer(required=False, description='Display Order'),
        'isCertipropane': fields.Boolean(required=False, description='Is Certipropane')
    })
    galleryImage_id = api.model('GalleryImage id', {
        'id': fields.Integer(required=True, description='The GalleryImage id')
    })
