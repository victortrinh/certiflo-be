import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.manufacturerImage import ManufacturerImage


def get_all_manufacturer_images():
    manufacturerImages = ManufacturerImage.query.all()
    return jsonify(manufacturerImages=[manufacturerImage.serialize() for manufacturerImage in manufacturerImages])


def save_new_manufacturer_image(data):
    new_manufacturer_image = ManufacturerImage(
        id=data['id'],
        manufacturerId=data['manufacturerId'],
        image=data['image']
    )
    save_changes(new_manufacturer_image)


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_manufacturer_image(data):
    manufacturer_image = ManufacturerImage.query.filter_by(id=data['id']).one()
    db.session.delete(manufacturer_image)
    db.session.commit()
    return {'message': "Manufacturer image id :" + str(data['id']) + " was deleted successfully"}, 200
