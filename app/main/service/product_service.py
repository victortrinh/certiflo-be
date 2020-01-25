import uuid
import datetime

from flask import jsonify
from app.main import db
from app.main.model.product import Product


def get_products():
    products = Product.query.all()
    return jsonify(products=[product.serialize() for product in products])


def save_new_product(data):
    new_product = Product(
        nameEn=data['nameEn'],
        nameFr=data['nameFr'],
        descriptionEn=data['descriptionEn'],
        descriptionFr=data['descriptionFr'],
        image=data['image']
    )
    save_changes(new_product)
    response_object = {
        'id': new_product.id,
    }
    return response_object, 201


def update_product(data):
    query = db.session.query(Product)
    query = query.filter(Product.id == data['id'])
    record = query.one()
    record.image = data["image"]
    record.nameEn = data["nameEn"]
    record.nameFr = data["nameFr"]
    record.descriptionEn = data["descriptionEn"]
    record.descriptionFr = data["descriptionFr"]
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


def delete_product(data):
    product = Product.query.filter_by(id=data['id']).one()
    db.session.delete(product)
    db.session.commit()
    return {'message': "product id :" + str(data['id']) + " was deleted successfully"}, 200
