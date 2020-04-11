from flask_restplus import Resource
from flask import request
from ..service.manufacturer_service import get_all_manufacturer, save_new_manufacturer, delete_manufacturer, update_manufacturers
from ..dto.manufacturer_dto import ManufacturerDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = ManufacturerDTO.api
auth = Auth.auth


@api.route('/all')
class Manufacturer(Resource):
    @api.doc('All manufacturers')
    def get(self):
        return get_all_manufacturer()


@api.route('/save')
class SaveManufacturer(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new manufacturer')
    @api.expect(ManufacturerDTO.manufacturer, validate=True)
    def post(self):
        data = request.json
        return save_new_manufacturer(data)


@api.route('/update')
class UpdateManufacturers(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update manufacturer')
    @api.expect([ManufacturerDTO.manufacturer], validate=True)
    def put(self):
        data = request.json
        return update_manufacturers(data)


@api.route('/delete')
class DeleteManufacturer(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete manufacturer')
    @api.expect(ManufacturerDTO.manufacturer_id, validate=True)
    def delete(self):
        data = request.json
        return delete_manufacturer(data)
