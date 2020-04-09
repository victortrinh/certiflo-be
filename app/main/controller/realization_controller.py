from flask_restplus import Resource
from flask import request
from ..service.realization_service import get_realizations, save_new_realization, update_realization, delete_realization, update_realizations
from ..dto.realization_dto import RealizationDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = RealizationDTO.api
auth = Auth.auth


@api.route('/all')
class GetRealizations(Resource):
    @api.doc('Get all realizations')
    def get(self):
        return get_realizations()


@api.route('/save')
class SaveRealization(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new realization')
    @api.expect(RealizationDTO.realization, validate=True)
    def post(self):
        data = request.json
        return save_new_realization(data)


@api.route('/update')
class UpdateRealization(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the realization')
    @api.expect(RealizationDTO.full_realization, validate=True)
    def put(self):
        data = request.json
        return update_realization(data)


@api.route('/updates')
class UpdateRealizations(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the realization')
    @api.expect([RealizationDTO.full_realization], validate=True)
    def put(self):
        data = request.json
        return update_realizations(data)


@api.route('/delete')
class DeleteRealization(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete realization')
    @api.expect(RealizationDTO.realization_id, validate=True)
    def delete(self):
        data = request.json
        return delete_realization(data)
