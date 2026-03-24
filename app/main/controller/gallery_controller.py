from flask_restx import Resource
from flask import request
from ..service.gallery_service import get_galleries, save_new_gallery, delete_gallery, update_galleries
from ..dto.gallery_dto import GalleryDTO

api = GalleryDTO.api


@api.route('/all')
class GetGalleries(Resource):
    @api.doc('Get galleries')
    def get(self):
        return get_galleries()


@api.route('/save')
class SaveGallery(Resource):
    @api.doc('Save new gallery')
    @api.expect(GalleryDTO.gallery, validate=True)
    def post(self):
        data = request.json
        return save_new_gallery(data)


@api.route('/update')
class UpdateGalleries(Resource):
    @api.doc('Update the gallery')
    @api.expect([GalleryDTO.full_gallery], validate=True)
    def put(self):
        data = request.json
        return update_galleries(data)


@api.route('/delete')
class DeleteGallery(Resource):
    @api.doc('Delete gallery')
    @api.expect(GalleryDTO.gallery_id, validate=True)
    def delete(self):
        data = request.json
        return delete_gallery(data)
