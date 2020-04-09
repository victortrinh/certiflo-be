import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.opening import Opening


def get_openings():
    openings = Opening.query.all()
    return jsonify(openings=[opening.serialize() for opening in openings])


def save_new_opening(data):
    new_opening = Opening(
        locationId=data['locationId'],
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        opening=data['opening'],
        closing=data['closing'],
        displayOrder=data['displayOrder'],
        isCertipropane=data['isCertipropane']
    )
    save_changes(new_opening)
    response_object = {
        'id': new_opening.id,
    }
    return response_object, 201


def update_opening(data):
    query = db.session.query(Opening)
    query = query.filter(Opening.id == data['id'])
    record = query.one()
    record.opening = data["opening"]
    record.closing = data["closing"]
    record.nameEn = data["nameEn"]
    record.nameFr = data["nameFr"]
    record.displayOrder = data["displayOrder"]
    record.isCertipropane = data["isCertipropane"]
    db.session.flush()
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully updated row.',
    }
    return response_object, 201


def update_openings(data):
    query = db.session.query(Opening)
    for opening in data:
        new_query = query.filter(Opening.id == opening['id'])
        record = new_query.one()
        record.opening = opening["opening"]
        record.closing = opening["closing"]
        record.nameEn = opening["nameEn"]
        record.nameFr = opening["nameFr"]
        record.displayOrder = opening["displayOrder"]
        record.isCertipropane = opening["isCertipropane"]
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


def delete_opening(data):
    opening = Opening.query.filter_by(id=data['id']).one()
    db.session.delete(opening)
    db.session.commit()
    return {'message': "Opening id :" + str(data['id']) + " was deleted successfully"}, 200
