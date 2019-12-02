from flask_restplus import Resource
from flask import request
from ..service.manufacturer_service import get_all_manufacturer, save_new_manufacturer, delete_manufacturer
from ..dto.manufacturer_dto import ManufacturerDTO


api = ManufacturerDTO.api


@api.route('/all')
class Manufacturer(Resource):
    @api.doc('All manufacturers')
    def get(self):
        return ManufacturerDTO()


@api.route('/save')
class SaveManufacturer(Resource):
    @api.doc('Save new manufacturer')
    @api.expect(ManufacturerDTO.manufacturer, validate=True)
    def post(self):
        data = request.json
        return save_new_manufacturer(data)


@api.route('/delete')
class DeleteManufacturer(Resource):
    @api.doc('Delete manufacturer')
    @api.expect(ManufacturerDTO.manufacturer_id, validate=True)
    def delete(self):
        data = request.json
        return delete_manufacturer(data)
