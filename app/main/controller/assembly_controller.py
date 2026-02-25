from flask_restx import Resource
from flask import request
from ..service.assembly_service import get_assemblies, save_new_assembly, delete_assembly, update_assemblies
from ..dto.assembly_dto import AssemblyDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = AssemblyDTO.api
auth = Auth.auth


@api.route('/all')
class GetAssemblies(Resource):
    @api.doc('Get assemblies')
    def get(self):
        return get_assemblies()


@api.route('/save')
class SaveAssembly(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new assembly')
    @api.expect(AssemblyDTO.assembly, validate=True)
    def post(self):
        data = request.json
        return save_new_assembly(data)


@api.route('/update')
class UpdateAssemblies(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the assembly')
    @api.expect([AssemblyDTO.full_assembly], validate=True)
    def put(self):
        data = request.json
        return update_assemblies(data)


@api.route('/delete')
class DeleteAssembly(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete assembly')
    @api.expect(AssemblyDTO.assembly_id, validate=True)
    def delete(self):
        data = request.json
        return delete_assembly(data)
