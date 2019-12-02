import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.manufacturer import Manufacturer


def get_all_manufacturer():
    manufacturers = Manufacturer.query.all()
    return jsonify(manufacturers=[manufacturer.serialize() for manufacturer in manufacturers])


def save_new_manufacturer(data):
    new_manufacturer = Manufacturer(
        nameEn=data['nameEn'],
        nameFr=data['nameFr']
    )
    save_changes(new_manufacturer)
    response_object = {
        'id': new_manufacturer.id,
    }
    return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_manufacturer(data):
    manufacturer = Manufacturer.query.filter_by(id=data['id']).one()
    db.session.delete(manufacturer)
    db.session.commit()
    return {'message': "Manufacturer id :" + str(data['id']) + " was deleted successfully"}, 200
