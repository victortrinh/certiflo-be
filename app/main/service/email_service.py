import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.email import Email


def get_emails():
    emails = Email.query.all()
    return jsonify(emails=[email.serialize() for email in emails])


def save_new_email(data):
    new_email = Email(
        locationId=data['locationId'],
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        email=data['email'],
        displayOrder=data['displayOrder'],
        isCertipropane=data['isCertipropane']
    )
    save_changes(new_email)
    response_object = {
        'id': new_email.id,
    }
    return response_object, 201


def update_email(data):
    query = db.session.query(Email)
    query = query.filter(Email.id == data['id'])
    record = query.one()
    record.email = data["email"]
    record.nameEn = data["nameEn"]
    record.nameFr = data["nameFr"]
    record.displayOrder = data["displayOrder"]
    record.isCertipropane = data["isCertipropane"]
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


def delete_email(data):
    email = Email.query.filter_by(id=data['id']).one()
    db.session.delete(email)
    db.session.commit()
    return {'message': "Email id :" + str(data['id']) + " was deleted successfully"}, 200
