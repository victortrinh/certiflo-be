#import uuid
#import datetime

from flask import jsonify
from app.main import db
from app.main.model.assembly import Assembly


def get_assemblies():
    assemblies = Assembly.query.all()
    return jsonify(assemblies=[assembly.serialize() for assembly in assemblies])


def save_new_assembly(data):
    new_assembly = Assembly(
        id=data['id'],
        assemblyTypeId=data['assemblyTypeId'],
        nameFr=data['nameFr'],
        nameEn=data['nameEn'],
        descriptionFr=data['descriptionFr'],
        descriptionEn=data['descriptionEn'],
        image=data['image']
    )
    save_changes(new_assembly)
    response_object = {
        'id': new_assembly.id,
    }
    return response_object, 201


def update_assembly(data):
    query = db.session.query(Assembly)
    query = query.filter(Assembly.id == data['id'])
    record = query.one()
    record.assemblyTypeId = data["assemblyTypeId"]
    record.nameFr = data["nameFr"]
    record.nameEn = data["nameEn"]
    record.descriptionFr = data["descriptionFr"]
    record.descriptionEn = data["descriptionEn"]
    record.image = data["image"]
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


def delete_assembly(data):
    assembly = Assembly.query.filter_by(id=data['id']).one()
    db.session.delete(assembly)
    db.session.commit()
    return {'message': "Assembly id :" + str(data['id']) + " was deleted successfully"}, 200
