from flask_restplus import Resource
from flask import request
from ..service.tanker_service import get_tankers, save_new_tanker, update_tanker, delete_tanker
from ..dto.tanker_dto import TankerDTO

api = TankerDTO.api


@api.route('/getAll')
class GetTankers(Resource):
    @api.doc('Get tankers')
    def get(self):
        return get_tankers()


@api.route('/save')
class SaveTanker(Resource):
    @api.doc('Save new tanker')
    @api.expect(TankerDTO.tanker, validate=True)
    def post(self):
        data = request.json
        return save_new_tanker(data)


@api.route('/update')
class UpdateTanker(Resource):
    @api.doc('Update the tanker')
    @api.expect(TankerDTO.full_tanker, validate=True)
    def put(self):
        data = request.json
        return update_tanker(data)


@api.route('/delete')
class DeleteTanker(Resource):
    @api.doc('Delete tanker')
    @api.expect(TankerDTO.tanker_id, validate=True)
    def delete(self):
        data = request.json
        return delete_tanker(data)
