import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.tanker import Tanker


def get_tankers():
    tankers = Tanker.query.all()
    return jsonify(tankers=[tanker.serialize() for tanker in tankers])


def save_new_tanker(data):
    new_tanker = Tanker(
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        unitId=data['unitId'],
        image=data['image'],
        kilometers=data['kilometers'],
        engineEn=data['engineEn'],
        engineFr=data['engineFr'],
        manufacturer=data['manufacturer'],
        year=data['year'],
        capacityInLitres=data['capacityInLitres'],
        capacity=data['capacity'],
        material=data['material'],
        noCompartments=data['noCompartments'],
        price=data['price'],
        dispenser=data['dispenser'],
        availability=data['availability'],
        cylinderRefill=data['cylinderRefill'],
        pump=data['pump'],
        additionalInformationEn=data['additionalInformationEn'],
        additionalInformationFr=data['additionalInformationFr'],
        displayOrder=data['displayOrder'],
        isCertipropane=data['isCertipropane']
    )
    save_changes(new_tanker)
    response_object = {
        'id': new_tanker.id,
    }
    return response_object, 201


def update_tankers(data):
    query = db.session.query(Tanker)
    for tanker in data:
        new_query = query.filter(Tanker.id == tanker['id'])
        record = new_query.one()
        record.nameEn = tanker["nameEn"]
        record.nameFr = tanker['nameFr']
        record.unitId = tanker['unitId']
        record.image = tanker['image']
        record.kilometers = tanker['kilometers']
        record.engineEn = tanker['engineEn']
        record.engineFr = tanker['engineFr']
        record.manufacturer = tanker['manufacturer']
        record.year = tanker['year']
        record.capacityInLitres = tanker['capacityInLitres']
        record.displayOrder = tanker["displayOrder"]
        record.isCertipropane = tanker["isCertipropane"]
        record.capacity = tanker['capacity']
        record.material = tanker['material']
        record.noCompartments = tanker['noCompartments']
        record.price = tanker['price']
        record.dispenser = tanker['dispenser']
        record.availability = tanker['availability']
        record.cylinderRefill = tanker['cylinderRefill']
        record.pump = tanker['pump']
        record.additionalInformationEn = tanker['additionalInformationEn']
        record.additionalInformationFr = tanker['additionalInformationFr']
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


def delete_tanker(data):
    tanker = Tanker.query.filter_by(id=data['id']).one()
    db.session.delete(tanker)
    db.session.commit()
    return {'message': "tanker id :" + str(data['id']) + " was deleted successfully"}, 200
