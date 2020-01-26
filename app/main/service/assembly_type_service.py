#import uuid
#import datetime

from flask import jsonify
from app.main import db
from app.main.model.assemblyType import AssemblyType


def get_assembly_types():
    assemblyTypes = AssemblyType.query.all()
    return jsonify(assemblyTypes=[assemblyTypes.serialize() for assemblyType in assemblyTypes])


def save_new_assembly_type(data):
    new_assemblyType = AssemblyType(
        id=data['id'],
        nameFr=data['nameFr'],
        nameEn=data['nameEn'],
    )
    save_changes(new_assemblyType)
    response_object = {
        'id': new_assemblyType.id,
    }
    return response_object, 201


def update_assembly_type(data):
    query = db.session.query(AssemblyType)
    query = query.filter(AssemblyType.id == data['id'])
    record = query.one()
    record.id = data["id"]
    record.nameFr = data["nameFr"]
    record.nameEn = data["nameEn"]
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


def delete_assembly_type(data):
    assemblyType = AssemblyType.query.filter_by(id=data['id']).one()
    db.session.delete(assemblyType)
    db.session.commit()
    return {'message': "Assembly type id :" + str(data['id']) + " was deleted successfully"}, 200
