import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.resource import Resource


def get_all_resources():
    resources = Resource.query.all()
    return jsonify(resources=[resource.serialize() for resource in resources])


def get_resources_by_language(language):
    resources = Resource.query.filter_by(language=language)
    return jsonify(resources=[resource.serialize() for resource in resources])


def get_resources_by_page_and_language(page, language):
    resources = Resource.query.filter_by(page=page, language=language)
    return jsonify(resources=[resource.serialize() for resource in resources])


def save_new_resource(data):
    new_resource = Resource(
        page=data['page'],
        language=data['language'],
        object_key=data['object_key'],
        resource=data['resource']
    )
    save_changes(new_resource)


def update_resource(data):
    query = db.session.query(Resource)
    query = query.filter(Resource.page == data['page'], Resource.language ==
                         data['language'], Resource.object_key == data['object_key'])
    record = query.one()
    record.resource = data["resource"]
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
