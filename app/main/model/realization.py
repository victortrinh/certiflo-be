from .. import db


class Realization(db.Model):
    __tablename__ = "realizations"

    id = db.Column(db.Integer, primary_key=True)
    realizationTypeId = db.Column(db.Integer, unique=False)
    descriptionFr = db.Column(db.String(255), unique=False)
    descriptionEn = db.Column(db.String(255), unique=False)
    projectTypeFr = db.Column(db.String(255), unique=False)
    projectTypeEn = db.Column(db.String(255), unique=False)
    image = db.Column(db.String(255), unique=False)
    specification = db.Column(db.String(255), unique=False)
    capacity = db.Column(db.String(255), unique=False)
    material = db.Column(db.String(255), unique=False)
    compartments = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Realization {}>'.format(self.specification)

    def serialize(self):
        return {
            'id': self.id,
            'realizationTypeId': self.realizationTypeId,
            'descriptionFr': self.descriptionFr,
            'descriptionEn': self.descriptionEn,
            'projectTypeFr': self.projectTypeFr,
            'projectTypeEn': self.projectTypeEn,
            'image': self.image,
            'specification': self.specification,
            'capacity': self.capacity,
            'material': self.material,
            'compartments': self.compartments
        }
