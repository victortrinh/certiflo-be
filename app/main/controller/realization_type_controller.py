from flask_restplus import Resource
from flask import request
from ..service.realization_type_service import get_realization_types, save_new_realization_type, update_realization_type, delete_realization_type, update_realization_types, update_realization_types
from ..dto.realization_type_dto import RealizationTypeDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = RealizationTypeDTO.api
auth = Auth.auth


@api.route('/all')
class GetRealizationTypes(Resource):
    @api.doc('Get all realization types')
    def get(self):
        return get_realization_types()


@api.route('/save')
class SaveRealizationType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new realization type')
    @api.expect(RealizationTypeDTO.realizationType, validate=True)
    def post(self):
        data = request.json
        return save_new_realization_type(data)


@api.route('/update')
class UpdateRealization(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the realization type')
    @api.expect(RealizationTypeDTO.full_realization_type, validate=True)
    def put(self):
        data = request.json
        return update_realization_type(data)


@api.route('/updates')
class UpdateRealizations(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the realization type')
    @api.expect([RealizationTypeDTO.full_realization_type], validate=True)
    def put(self):
        data = request.json
        return update_realization_types(data)


@api.route('/delete')
class DeleteRealization(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete realization type')
    @api.expect(RealizationTypeDTO.realization_type_id, validate=True)
    def delete(self):
        data = request.json
        return delete_realization_type(data)
