from .. import db


class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id = db.Column(db.Integer, primary_key=True)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Manufacturer {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr
        }
