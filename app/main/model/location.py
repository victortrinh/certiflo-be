from .. import db


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    address = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Location {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'address': self.address
        }
