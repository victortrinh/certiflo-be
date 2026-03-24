from .. import db


class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id = db.Column(db.Integer, primary_key=True)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    images = db.relationship('ManufacturerImage', backref='manufacturer', cascade='all, delete-orphan', passive_deletes=True, lazy=True)

    def __repr__(self):
        return '<Manufacturer {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'displayOrder': self.displayOrder
        }
