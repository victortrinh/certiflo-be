from flask_restplus import Resource
from flask import request
from ..service.realization_type_service import get_realization_types, save_new_realization_type, update_realization_type, delete_realization_type
from ..dto.realization_type_dto import RealizationTypeDTO


api = RealizationTypeDTO.api


@api.route('/getAll')
class GetRealizationTypes(Resource):
    @api.doc('Get all realization types')
    def get(self):
        return get_realization_types()


@api.route('/save')
class SaveRealizationType(Resource):
    @api.doc('Save new realization type')
    @api.expect(RealizationTypeDTO.realizationType, validate=True)
    def post(self):
        data = request.json
        return save_new_realization_type(data)


@api.route('/update')
class UpdateRealization(Resource):
    @api.doc('Update the realization type')
    @api.expect(RealizationTypeDTO.full_realization_type, validate=True)
    def put(self):
        data = request.json
        return update_realization_type(data)


@api.route('/delete')
class DeleteRealization(Resource):
    @api.doc('Delete realization type')
    @api.expect(RealizationTypeDTO.realization_type_id, validate=True)
    def delete(self):
        data = request.json
        return delete_realization_type(data)
