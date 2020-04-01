from .. import db


class Telephone(db.Model):
    __tablename__ = "telephones"

    id = db.Column(db.Integer, primary_key=True)
    locationId = db.Column(db.String(255), unique=False)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    telephone = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Telephone {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'locationId': self.locationId,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'telephone': self.telephone,
            'displayOrder': self.displayOrder
        }
