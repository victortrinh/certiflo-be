import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.gallery import Gallery


def get_galleries():
    galleries = Gallery.query.all()
    return jsonify(galleries=[gallery.serialize() for gallery in galleries])


def save_new_gallery(data):
    new_gallery = Gallery(
        company=data['company'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_gallery)
    response_object = {
        'id': new_gallery.id,
    }
    return response_object, 201


def update_galleries(data):
    query = db.session.query(Gallery)
    for gallery in data:
        new_query = query.filter(Gallery.id == gallery['id'])
        record = new_query.one()
        record.company = gallery["company"]
        record.displayOrder = gallery["displayOrder"]
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


def delete_gallery(data):
    gallery = Gallery.query.filter_by(id=data['id']).one()
    db.session.delete(gallery)
    db.session.commit()
    return {'message': "gallery id :" + str(data['id']) + " was deleted successfully"}, 200
