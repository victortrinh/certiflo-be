from flask_restplus import Resource
from flask import request
from ..service.location_service import get_all_locations, save_new_location, delete_location, update_locations
from ..dto.location_dto import LocationDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = LocationDTO.api
auth = Auth.auth


@api.route('/all')
class Location(Resource):
    @api.doc('All Location')
    def get(self):
        return get_all_locations()


@api.route('/save')
class SaveLocation(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new location')
    @api.expect(LocationDTO.location, validate=True)
    def post(self):
        data = request.json
        return save_new_location(data)


@api.route('/update')
class UpdateLocations(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the location')
    @api.expect([LocationDTO.location], validate=True)
    def put(self):
        data = request.json
        return update_locations(data)


@api.route('/delete')
class DeleteLocation(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete location')
    @api.expect(LocationDTO.location_id, validate=True)
    def delete(self):
        data = request.json
        return delete_location(data)
