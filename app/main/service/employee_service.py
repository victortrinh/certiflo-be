import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.employee import Employee


def get_employees():
    employees = Employee.query.all()
    return jsonify(employees=[employee.serialize() for employee in employees])


def save_new_employee(data):
    new_employee = Employee(
        firstName=data['firstName'],
        lastName=data['lastName'],
        roleFr=data['roleFr'],
        roleEn=data['roleEn'],
        email=data['email'],
        company=data['company'],
        image=data['image'],
        descriptionFr=data['descriptionFr'],
        descriptionEn=data['descriptionEn'],
        displayOrder=data['displayOrder']
    )
    save_changes(new_employee)
    response_object = {
        'id': new_employee.id,
    }
    return response_object, 201


def update_employees(data):
    query = db.session.query(Employee)
    for employee in data:
        new_query = query.filter(Employee.id == employee['id'])
        record = new_query.one()
        record.firstName = employee["firstName"]
        record.lastName = employee["lastName"]
        record.roleFr = employee["roleFr"]
        record.roleEn = employee["roleEn"]
        record.email = employee["email"]
        record.company = employee['company']
        record.image = employee["image"]
        record.descriptionFr = employee["descriptionFr"]
        record.descriptionEn = employee["descriptionEn"]
        record.displayOrder = employee["displayOrder"]
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


def delete_employee(data):
    employee = Employee.query.filter_by(id=data['id']).one()
    db.session.delete(employee)
    db.session.commit()
    return {'message': "Employee id :" + str(data['id']) + " was deleted successfully"}, 200
