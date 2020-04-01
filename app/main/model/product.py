from .. import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), unique=False)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    descriptionEn = db.Column(db.Text, unique=False)
    descriptionFr = db.Column(db.Text, unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Product {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'image': self.image,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'descriptionEn': self.descriptionEn,
            'descriptionFr': self.descriptionFr,
            'displayOrder': self.displayOrder
        }
