import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.galleryImage import GalleryImage


def get_galleryImages(id):
    galleryImages = GalleryImage.query.all()
    return jsonify(galleryImages=[galleryImage.serialize() for galleryImage in galleryImages])


def save_new_galleryImage(data):
    new_galleryImage = GalleryImage(
        image=data['image'],
        galleryId=data['galleryId']
    )
    save_changes(new_galleryImage)
    response_object = {
        'id': new_galleryImage.id,
    }
    return response_object, 201


def update_galleryImage(data):
    query = db.session.query(GalleryImage)
    query = query.filter(GalleryImage.id == data['id'])
    record = query.one()
    record.galleryId = data["galleryId"]
    record.image = data["image"]
    db.session.flush()
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully updated row.',
    }
    return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_galleryImage(data):
    galleryImage = GalleryImage.query.filter_by(id=data['id']).one()
    db.session.delete(galleryImage)
    db.session.commit()
    return {'message': "galleryImage id :" + str(data['id']) + " was deleted successfully"}, 200
