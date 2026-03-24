from flask_restx import Resource
from flask import request
from ..dto.all_dto import AllDTO
from ..service.all_service import get_all

api = AllDTO.api


@api.route('/')
class GetAll(Resource):
    @api.doc('Get all')
    def get(self):
        return get_all()
