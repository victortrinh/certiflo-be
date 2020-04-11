from flask_restplus import Resource
from flask import request
from ..service.gallery_image_service import get_galleryImages, save_new_galleryImage, delete_galleryImage, update_galleryImages
from ..dto.gallery_image_dto import GalleryImageDTO

api = GalleryImageDTO.api


@api.route('/all')
class GetGalleryImages(Resource):
    @api.doc('Get galleries')
    def get(self):
        return get_galleryImages()


@api.route('/save')
class SaveGalleryImage(Resource):
    @api.doc('Save new galleryImage')
    @api.expect(GalleryImageDTO.galleryImage, validate=True)
    def post(self):
        data = request.json
        return save_new_galleryImage(data)


@api.route('/update')
class UpdateGalleryImages(Resource):
    @api.doc('Update the galleryImage')
    @api.expect([GalleryImageDTO.full_galleryImage], validate=True)
    def put(self):
        data = request.json
        return update_galleryImages(data)


@api.route('/delete')
class DeleteGalleryImage(Resource):
    @api.doc('Delete galleryImage')
    @api.expect(GalleryImageDTO.galleryImage_id, validate=True)
    def delete(self):
        data = request.json
        return delete_galleryImage(data)
