from flask_restplus import Namespace, fields


class AssemblyDTO:
    api = Namespace('Assembly', description='Assembly related operations')
    assembly = api.model('Assembly', {
        'assemblyTypeId': fields.Integer(required=True, description='The related assembly type id'),
        'nameEn': fields.String(required=True, description='Assembly name in french'),
        'nameFr': fields.String(required=True, description='Assembly name in english'),
        'image': fields.String(required=True, description='Image'),
        'descriptionEn': fields.String(required=True, description='Assembly description in english'),
        'descriptionFr': fields.String(required=True, description='Assembly description in french'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    full_assembly = api.model('Full assembly', {
        'id': fields.Integer(required=True, description='The assembly id'),
        'assemblyTypeId': fields.Integer(required=True, description='The related assembly type id'),
        'nameEn': fields.String(required=True, description='Assembly name in french'),
        'nameFr': fields.String(required=True, description='Assembly name in english'),
        'image': fields.String(required=True, description='Image'),
        'descriptionEn': fields.String(required=True, description='Assembly description in english'),
        'descriptionFr': fields.String(required=True, description='Assembly description in french'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    assembly_id = api.model('Assembly id', {
        'id': fields.Integer(required=True, description='The assembly id'),
    })
