from flask_restx import Resource, Namespace
from flask import request
from ..service.resources_service import get_all_resources, get_resources_by_page_and_language, save_new_resource, update_resource, get_resources_by_language, delete_resource, update_resource_by_id_and_language
from ..dto.resources_dto import ResourceDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = ResourceDTO.api
auth = Auth.auth


@api.route('/all')
class Resources(Resource):
    @api.doc('All resources')
    def get(self):
        return get_all_resources()


@api.route('/<language>')
class GetResourceByLanguage(Resource):
    @api.doc('Get resource by language')
    def get(self, language):
        return get_resources_by_language(language)


@api.route('/<page>/<language>')
class GetResourceByPageAndLanguage(Resource):
    @api.doc('Get resource by page and language')
    def get(self, page, language):
        return get_resources_by_page_and_language(page, language)


@api.route('/update')
class UpdateResource(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the resource')
    @api.expect(ResourceDTO.resource, validate=True)
    def put(self):
        data = request.json
        return update_resource(data)


@api.route('/updateById')
class UpdateResource(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the resource by id')
    @api.expect(ResourceDTO.resource_id_language, validate=True)
    def put(self):
        data = request.json
        return update_resource_by_id_and_language(data)


@api.route('/save')
class SaveResource(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new resource')
    @api.expect(ResourceDTO.resource, validate=True)
    def post(self):
        data = request.json
        return save_new_resource(data)


@api.route('/delete')
class DeleteResource(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete resource')
    @api.expect(ResourceDTO.resource_id, validate=True)
    def delete(self):
        data = request.json
        return delete_resource(data)
