import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.realization import Realization


def get_realizations():
    realizations = Realization.query.all()
    return jsonify(realizations=[realization.serialize() for realization in realizations])


def save_new_realization(data):
    new_realization = Realization(
        realizationTypeId=data['realizationTypeId'],
        descriptionEn=data['descriptionEn'],
        descriptionFr=data['descriptionFr'],
        projectTypeFr=data['projectTypeFr'],
        projectTypeEn=data['projectTypeEn'],
        image=data['image'],
        specification=data['specification'],
        capacity=data['capacity'],
        material=data['material'],
        compartments=data['compartments'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_realization)
    response_object = {
        'id': new_realization.id,
    }
    return response_object, 201


def update_realization(data):
    query = db.session.query(Realization)
    query = query.filter(Realization.id == data['id'])
    record = query.one()
    record.image = data["image"]
    record.realizationTypeId = data["realizationTypeId"]
    record.descriptionEn = data["descriptionEn"]
    record.descriptionFr = data["descriptionFr"]
    record.projectTypeFr = data["projectTypeFr"]
    record.projectTypeEn = data["projectTypeEn"]
    record.specification = data["specification"]
    record.displayOrder = data["displayOrder"]
    record.capacity = data["capacity"]
    record.material = data["material"]
    record.compartments = data["compartments"]
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


def delete_realization(data):
    realization = Realization.query.filter_by(id=data['id']).one()
    db.session.delete(realization)
    db.session.commit()
    return {'message': "Realization id :" + str(data['id']) + " was deleted successfully"}, 200
