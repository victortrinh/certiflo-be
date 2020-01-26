from flask_restplus import Resource
from flask import request
from ..service.assembly_service import get_assemblies, save_new_assembly, update_assembly, delete_assembly
from ..dto.assembly_dto import AssemblyDTO

api = AssemblyDTO.api


@api.route('/getAll')
class GetAssemblies(Resource):
    @api.doc('Get assemblies')
    def get(self):
        return get_assemblies()


@api.route('/save')
class SaveAssembly(Resource):
    @api.doc('Save new assembly')
    @api.expect(AssemblyDTO.assembly, validate=True)
    def post(self):
        data = request.json
        return save_new_assembly(data)


@api.route('/update')
class UpdateAssembly(Resource):
    @api.doc('Update the assembly')
    @api.expect(AssemblyDTO.full_assembly, validate=True)
    def put(self):
        data = request.json
        return update_assembly(data)


@api.route('/delete')
class DeleteAssembly(Resource):
    @api.doc('Delete assembly')
    @api.expect(AssemblyDTO.assembly_id, validate=True)
    def delete(self):
        data = request.json
        return delete_assembly(data)
