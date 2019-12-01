import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.location import Location


def get_all_locations():
    locations = Location.query.all()
    return jsonify(locations=[location.serialize() for location in locations])


def save_new_location(data):
    new_location = Location(
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        address=data['address']
    )
    save_changes(new_location)


def update_location(data):
    query = db.session.query(Location)
    query = query.filter(Location.id == data['id'])
    record = query.one()
    record.address = data["address"]
    record.nameEn = data["nameEn"]
    record.nameFr = data["nameFr"]
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


def delete_location(data):
    location = Location.query.filter_by(id=data['id']).one()
    db.session.delete(location)
    db.session.commit()
    return {'message': "Location id :" + str(data['id']) + " was deleted successfully"}, 200
