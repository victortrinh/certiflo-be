from flask_restplus import Namespace, fields


class RealizationTypeDTO:
    api = Namespace(
        'Realization Type', description='Realization Type related operations')
    realizationType = api.model('realizationType', {
        'realizationTypeEn': fields.String(required=True, description='RealizationType'),
        'realizationTypeFr': fields.String(required=True, description='RealizationType'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    full_realization_type = api.model('Full realization type', {
        'id': fields.Integer(required=True, description='The id'),
        'realizationTypeEn': fields.String(required=True, description='RealizationType'),
        'realizationTypeFr': fields.String(required=True, description='RealizationType'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    realization_type_id = api.model('Realization id', {
        'id': fields.Integer(required=True, description='The realization type id'),
    })
