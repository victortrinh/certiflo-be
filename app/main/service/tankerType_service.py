import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.tankerType import TankerType


def get_tankerTypes():
    tankerTypes = TankerType.query.all()
    return jsonify(tankerTypes=[tankerType.serialize() for tankerType in tankerTypes])


def save_new_tankerType(data):
    new_tankerType = TankerType(
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_tankerType)
    response_object = {
        'id': new_tankerType.id,
    }
    return response_object, 201


def update_tankerType(data):
    query = db.session.query(TankerType)
    query = query.filter(TankerType.id == data['id'])
    record = query.one()
    record.nameEn = data["nameEn"]
    record.nameFr = data["nameFr"]
    record.displayOrder = data["displayOrder"]
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


def delete_tankerType(data):
    tankerType = TankerType.query.filter_by(id=data['id']).one()
    db.session.delete(tankerType)
    db.session.commit()
    return {'message': "tankerType id :" + str(data['id']) + " was deleted successfully"}, 200
