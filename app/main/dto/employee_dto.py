from flask_restplus import Namespace, fields


class EmployeeDTO:
    api = Namespace('Employee', description='Employee related operations')
    employee = api.model('employee', {
        'firstName': fields.String(required=True, description='First name'),
        'lastName': fields.String(required=True, description='Last name'),
        'roleFr': fields.String(required=True, description='Role in french'),
        'roleEn': fields.String(required=True, description='Role in english'),
        'email': fields.String(required=True, description='Email'),
        'image': fields.String(required=True, description='Photo'),
        'description': fields.String(required=True, description='Description')
    })
    full_employee = api.model('Full employee', {
        'id': fields.Integer(required=True, description='Id'),
        'firstName': fields.String(required=True, description='First name'),
        'lastName': fields.String(required=True, description='Last name'),
        'roleFr': fields.String(required=True, description='Role in french'),
        'roleEn': fields.String(required=True, description='Role in english'),
        'email': fields.String(required=True, description='Email'),
        'image': fields.String(required=True, description='Photo'),
        'description': fields.String(required=True, description='Description')
    })
    employee_id = api.model('Employee id', {
        'id': fields.Integer(required=True, description='The id'),
    })
