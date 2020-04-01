from .. import db


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    locationId = db.Column(db.String(255), unique=False)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    email = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Email {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'locationId': self.locationId,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'email': self.email,
            'displayOrder': self.displayOrder
        }
