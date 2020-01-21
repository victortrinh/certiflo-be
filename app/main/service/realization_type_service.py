import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.realizationType import RealizationType


def get_realization_types():
    realizationTypes = RealizationType.query.all()
    return jsonify(realizationTypes=[realizationType.serialize() for realizationType in realizationTypes])


def save_new_realization_type(data):
    new_realization_type = RealizationType(
        realizationTypeFr=data['realizationTypeFr'],
        realizationTypeEn=data['realizationTypeEn']
    )
    save_changes(new_realization_type)
    response_object = {
        'id': new_realization_type.id,
    }
    return response_object, 201


def update_realization_type(data):
    query = db.session.query(RealizationType)
    query = query.filter(RealizationType.id == data['id'])
    record = query.one()
    record.realizationTypeEn = data["realizationTypeEn"]
    record.realizationTypeFr = data["realizationTypeFr"]
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


def delete_realization_type(data):
    realizationType = RealizationType.query.filter_by(id=data['id']).one()
    db.session.delete(realizationType)
    db.session.commit()
    return {'message': "Realization type id :" + str(data['id']) + " was deleted successfully"}, 200
