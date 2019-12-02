from flask_restplus import Resource
from flask import request
from ..service.opening_service import get_openings, save_new_opening, update_opening, delete_opening
from ..dto.opening_dto import OpeningDTO

api = OpeningDTO.api


@api.route('/getAll')
class GetOpenings(Resource):
    @api.doc('Get openings')
    def get(self):
        return get_openings()


@api.route('/save')
class SaveOpening(Resource):
    @api.doc('Save new opening')
    @api.expect(OpeningDTO.opening, validate=True)
    def post(self):
        data = request.json
        return save_new_opening(data)


@api.route('/update')
class UpdateOpening(Resource):
    @api.doc('Update the opening')
    @api.expect(OpeningDTO.full_opening, validate=True)
    def put(self):
        data = request.json
        return update_opening(data)


@api.route('/delete')
class DeleteOpening(Resource):
    @api.doc('Delete opening')
    @api.expect(OpeningDTO.opening_id, validate=True)
    def delete(self):
        data = request.json
        return delete_opening(data)
