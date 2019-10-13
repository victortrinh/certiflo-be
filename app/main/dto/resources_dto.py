from flask_restplus import Namespace, fields


class ResourceDTO:
    api = Namespace('Resource', description='Resources related operations')
    resource_page_language = api.model('resource', {
        'language': fields.String(required=True, description='resource language'),
        'page': fields.String(required=True, description='resource page')
    })
    resource = api.model('resource', {
        'language': fields.String(required=True, description='resource language'),
        'page': fields.String(required=True, description='resource page'),
        'object_key': fields.String(required=True, description='resource key'),
        'resource': fields.String(required=True, description='resource')
    })
