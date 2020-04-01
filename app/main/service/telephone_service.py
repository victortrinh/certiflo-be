import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.telephone import Telephone


def get_telephones():
    telephones = Telephone.query.all()
    return jsonify(telephones=[telephone.serialize() for telephone in telephones])


def save_new_telephone(data):
    new_telephone = Telephone(
        locationId=data['locationId'],
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        telephone=data['telephone'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_telephone)
    response_object = {
        'id': new_telephone.id,
    }
    return response_object, 201


def update_telephone(data):
    query = db.session.query(Telephone)
    query = query.filter(Telephone.id == data['id'])
    record = query.one()
    record.telephone = data["telephone"]
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


def delete_telephone(data):
    telephone = Telephone.query.filter_by(id=data['id']).one()
    db.session.delete(telephone)
    db.session.commit()
    return {'message': "Telephone id :" + str(data['id']) + " was deleted successfully"}, 200
