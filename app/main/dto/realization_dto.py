from flask_restplus import Namespace, fields


class RealizationDTO:
    api = Namespace(
        'Realization', description='Realization related operations')
    realization = api.model('realization', {
        'realizationTypeId': fields.Integer(required=True, description='The realization type id'),
        'descriptionFr': fields.String(required=True, description='The project type in french'),
        'descriptionEn': fields.String(required=True, description='The project type in english'),
        'projectTypeFr': fields.String(required=True, description='The project type in french'),
        'projectTypeEn': fields.String(required=True, description='The project type in english'),
        'image': fields.String(required=True, description='The image'),
        'specification': fields.String(required=True, description='Specification'),
        'capacity': fields.String(required=True, description='Capacity'),
        'material': fields.String(required=True, description='Material'),
        'compartments': fields.String(required=True, description='Compartments')
    })
    full_realization = api.model('Full realization', {
        'id': fields.Integer(required=True, description='The id'),
        'realizationTypeId': fields.Integer(required=True, description='The realization type id'),
        'descriptionFr': fields.String(required=True, description='The project type in french'),
        'descriptionEn': fields.String(required=True, description='The project type in english'),
        'projectTypeFr': fields.String(required=True, description='The project type in french'),
        'projectTypeEn': fields.String(required=True, description='The project type in english'),
        'image': fields.String(required=True, description='The image'),
        'specification': fields.String(required=True, description='Specification'),
        'capacity': fields.String(required=True, description='Capacity'),
        'material': fields.String(required=True, description='Material'),
        'compartments': fields.String(required=True, description='Compartments')
    })
    realization_id = api.model('Realization id', {
        'id': fields.Integer(required=True, description='The realization id'),
    })
