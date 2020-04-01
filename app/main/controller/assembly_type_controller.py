from flask_restplus import Resource
from flask import request
from ..service.assembly_type_service import get_assembly_types, save_new_assembly_type, update_assembly_type, delete_assembly_type
from ..dto.assembly_type_dto import AssemblyTypeDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = AssemblyTypeDTO.api
auth = Auth.auth


@api.route('/all')
class GetAssemblyTypes(Resource):
    @api.doc('Get assembly types')
    def get(self):
        return get_assembly_types()


@api.route('/save')
class SaveAssemblyType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new assembly type')
    @api.expect(AssemblyTypeDTO.assembly_type, validate=True)
    def post(self):
        data = request.json
        return save_new_assembly_type(data)


@api.route('/update')
class UpdateAssemblyType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the assembly type')
    @api.expect(AssemblyTypeDTO.full_assembly_type, validate=True)
    def put(self):
        data = request.json
        return update_assembly_type(data)


@api.route('/delete')
class DeleteAssemblyType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete assembly')
    @api.expect(AssemblyTypeDTO.assembly_type_id, validate=True)
    def delete(self):
        data = request.json
        return delete_assembly_type(data)
