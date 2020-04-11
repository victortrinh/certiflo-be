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
        displayOrder=data['displayOrder'],
        isCertipropane=data['isCertipropane']
    )
    save_changes(new_realization)
    response_object = {
        'id': new_realization.id,
    }
    return response_object, 201


def update_realizations(data):
    query = db.session.query(Realization)
    for realization in data:
        new_query = query.filter(Realization.id == realization['id'])
        record = new_query.one()
        record.image = realization["image"]
        record.realizationTypeId = realization["realizationTypeId"]
        record.descriptionEn = realization["descriptionEn"]
        record.descriptionFr = realization["descriptionFr"]
        record.projectTypeFr = realization["projectTypeFr"]
        record.projectTypeEn = realization["projectTypeEn"]
        record.specification = realization["specification"]
        record.displayOrder = realization["displayOrder"]
        record.capacity = realization["capacity"]
        record.material = realization["material"]
        record.compartments = realization["compartments"]
        record.isCertipropane = realization["isCertipropane"]
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
