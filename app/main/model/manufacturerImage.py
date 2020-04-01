from .. import db


class ManufacturerImage(db.Model):
    __tablename__ = "manufacturerImages"

    id = db.Column(db.Integer, primary_key=True)
    manufacturerId = db.Column(db.Integer, unique=False)
    image = db.Column(db.Text, unique=False)
    descriptionEn = db.Column(db.Text, unique=False)
    descriptionFr = db.Column(db.Text, unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<ManufacturerImage {}>'.format(self.manufacturerId)

    def serialize(self):
        return {
            'id': self.id,
            'manufacturerId': self.manufacturerId,
            'image': self.image,
            'descriptionEn': self.descriptionEn,
            'descriptionFr': self.descriptionFr,
            'displayOrder': self.displayOrder
        }
