from flask_restplus import Namespace, fields


class AssemblyTypeDTO:
    api = Namespace(
        'AssemblyType', description='Assembly Type related operations')
    assembly_type = api.model('Assembly type', {
        'nameEn': fields.String(required=True, description='Assembly type name in french'),
        'nameFr': fields.String(required=True, description='Assembly type name in english'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    full_assembly_type = api.model('Full assembly type', {
        'id': fields.Integer(required=True, description='The assembly type id'),
        'nameEn': fields.String(required=True, description='Assembly type name in french'),
        'nameFr': fields.String(required=True, description='Assembly type name in english'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    assembly_type_id = api.model('Assembly type id', {
        'id': fields.Integer(required=True, description='The assembly type id'),
    })
