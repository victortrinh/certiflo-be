from flask_restplus import Resource
from flask import request
from ..service.manufacturerImage_service import get_all_manufacturer_images, save_new_manufacturer_image, delete_manufacturer_image, update_manufacturer_image
from ..dto.manufacturerImage_dto import ManufacturerImageDTO


api = ManufacturerImageDTO.api


@api.route('/all')
class ManufacturerImage(Resource):
    @api.doc('All manufacturer images')
    def get(self):
        return get_all_manufacturer_images()


@api.route('/save')
class SaveManufacturerImage(Resource):
    @api.doc('Save new manufacturer image')
    @api.expect(ManufacturerImageDTO.manufacturerImage, validate=True)
    def post(self):
        data = request.json
        return save_new_manufacturer_image(data)

@api.route('/update')
class UpdateManufacturerImage(Resource):
    @api.doc('Update manufacturer image')
    @api.expect(ManufacturerImageDTO.manufacturerImage, validate=True)
    def put(self):
        data = request.json
        return update_manufacturer_image(data)


@api.route('/delete')
class DeleteManufacturerImage(Resource):
    @api.doc('Delete manufacturer image')
    @api.expect(ManufacturerImageDTO.manufacturerImageId, validate=True)
    def delete(self):
        data = request.json
        return delete_manufacturer_image(data)
