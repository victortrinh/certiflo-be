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
        displayOrder=data['displayOrder']
    )
    save_changes(new_tanker)
    response_object = {
        'id': new_tanker.id,
    }
    return response_object, 201


def update_tanker(data):
    query = db.session.query(Tanker)
    query = query.filter(Tanker.id == data['id'])
    record = query.one()
    record.nameEn = data["nameEn"]
    record.nameFr = data['nameFr']
    record.unitId = data['unitId']
    record.image = data['image']
    record.kilometers = data['kilometers']
    record.engineEn = data['engineEn']
    record.engineFr = data['engineFr']
    record.manufacturer = data['manufacturer']
    record.year = data['year']
    record.capacityInLitres = data['capacityInLitres']
    record.displayOrder = data["displayOrder"]
    record.capacity = data['capacity']
    record.material = data['material']
    record.noCompartments = data['noCompartments']
    record.price = data['price']
    record.dispenser = data['dispenser']
    record.availability = data['availability']
    record.cylinderRefill = data['cylinderRefill']
    record.pump = data['pump']
    record.additionalInformationEn = data['additionalInformationEn']
    record.additionalInformationFr = data['additionalInformationFr']
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
