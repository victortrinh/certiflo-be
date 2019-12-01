from flask_restplus import Resource
from flask import request
from ..service.telephone_service import get_telephones_by_location_id, save_new_telephone, update_telephone, delete_telephone
from ..dto.telephone_dto import TelephoneDTO


api = TelephoneDTO.api


@api.route('/<locationId>')
class GetTelephonesByLocationId(Resource):
    @api.doc('Get telephones by location id')
    def get(self, locationId):
        return get_telephones_by_location_id(locationId)


@api.route('/save')
class SaveTelephone(Resource):
    @api.doc('Save new telephone')
    @api.expect(TelephoneDTO.telephone, validate=True)
    def post(self):
        data = request.json
        return save_new_telephone(data)


@api.route('/update')
class UpdateTelephone(Resource):
    @api.doc('Update the telephone')
    @api.expect(TelephoneDTO.telephone, validate=True)
    def put(self):
        data = request.json
        return update_telephone(data)


@api.route('/delete')
class DeleteTelephone(Resource):
    @api.doc('Delete telephone')
    @api.expect(TelephoneDTO.telephone_id, validate=True)
    def delete(self):
        data = request.json
        return delete_telephone(data)
