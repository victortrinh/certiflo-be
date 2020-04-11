#import uuid
#import datetime

from flask import jsonify
from app.main import db
from app.main.model.assemblyType import AssemblyType


def get_assembly_types():
    assemblyTypes = AssemblyType.query.all()
    return jsonify(assemblyTypes=[assemblyType.serialize() for assemblyType in assemblyTypes])


def save_new_assembly_type(data):
    new_assemblyType = AssemblyType(
        nameFr=data['nameFr'],
        nameEn=data['nameEn'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_assemblyType)
    response_object = {
        'id': new_assemblyType.id,
    }
    return response_object, 201


def update_assembly_types(data):
    query = db.session.query(AssemblyType)
    for assembly_type in data:
        new_query = query.filter(AssemblyType.id == assembly_type['id'])
        record = new_query.one()
        record.id = assembly_type["id"]
        record.nameFr = assembly_type["nameFr"]
        record.nameEn = assembly_type["nameEn"]
        record.displayOrder = assembly_type["displayOrder"]
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
