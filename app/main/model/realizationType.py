from .. import db


class RealizationType(db.Model):
    __tablename__ = "realizationTypes"

    id = db.Column(db.Integer, primary_key=True)
    realizationTypeEn = db.Column(db.String(255), unique=False)
    realizationTypeFr = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    realizations = db.relationship('Realization', backref='realization_type', cascade='all, delete-orphan', passive_deletes=True, lazy=True)

    def __repr__(self):
        return '<RealizationType {}>'.format(self.realisationTypeEn)

    def serialize(self):
        return {
            'id': self.id,
            'realizationTypeEn': self.realizationTypeEn,
            'realizationTypeFr': self.realizationTypeFr,
            'displayOrder': self.displayOrder
        }
