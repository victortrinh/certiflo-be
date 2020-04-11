from flask_restplus import Resource
from flask import request
from ..service.tankerType_service import get_tankerTypes, save_new_tankerType, delete_tankerType, update_tankerTypes
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth
from ..dto.tanker_type_dto import TankerTypeDTO

api = TankerTypeDTO.api
auth = Auth.auth


@api.route('/all')
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
class UpdateTankerTypes(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the tankerType')
    @api.expect([TankerTypeDTO.full_tankerType], validate=True)
    def put(self):
        data = request.json
        return update_tankerTypes(data)


@api.route('/delete')
class DeleteTankerType(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete tankerType')
    @api.expect(TankerTypeDTO.tankerType_id, validate=True)
    def delete(self):
        data = request.json
        return delete_tankerType(data)
