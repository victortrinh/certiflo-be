from .. import db


class ManufacturerImage(db.Model):
    __tablename__ = "manufacturerImages"

    id = db.Column(db.Integer, primary_key=True)
    manufacturerId = db.Column(db.Integer, unique=False)
    image = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<ManufacturerImage {}>'.format(self.manufacturerId)

    def serialize(self):
        return {
            'id': self.id,
            'manufacturerId': self.manufacturerId,
            'image': self.image
        }
