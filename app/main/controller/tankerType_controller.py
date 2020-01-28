from flask_restplus import Resource
from flask import request
from ..service.tankerType_service import get_tankerTypes, save_new_tankerType, update_tankerType, delete_tankerType
from ..dto.tankerType_dto import TankerTypeDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = TankerTypeDTO.api
auth = Auth.auth


@api.route('/getAll')
class GetTankerTypes(Resource):
    @api.doc('Get tankerTypes')
    def get(self):
        return get_tankerTypes()


@api.route('/save')
class SaveTankerType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new tankerType')
    @api.expect(TankerTypeDTO.tankerType, validate=True)
    def post(self):
        data = request.json
        return save_new_tankerType(data)


@api.route('/update')
class UpdateTankerType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the tankerType')
    @api.expect(TankerTypeDTO.full_tankerType, validate=True)
    def put(self):
        data = request.json
        return update_tankerType(data)


@api.route('/delete')
class DeleteTankerType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete tankerType')
    @api.expect(TankerTypeDTO.tankerType_id, validate=True)
    def delete(self):
        data = request.json
        return delete_tankerType(data)
