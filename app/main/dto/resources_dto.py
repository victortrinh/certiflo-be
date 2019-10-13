from flask_restplus import Namespace, fields


class ResourceDTO:
    api = Namespace('Resource', description='Resources related operations')
    resource_id = api.model('Resource id', {
        'id': fields.Integer(required=True, description='The resource id'),
    })
    resource_id_language = api.model('Resource id and language', {
        'id': fields.Integer(required=True, description='The resource id'),
        'language': fields.String(required=True, description='resource language')
    })
    resource = api.model('resource', {
        'language': fields.String(required=True, description='resource language'),
        'page': fields.String(required=True, description='resource page'),
        'object_key': fields.String(required=True, description='resource key'),
        'resource': fields.String(required=True, description='resource')
    })
