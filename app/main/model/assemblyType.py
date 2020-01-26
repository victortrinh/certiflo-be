from .. import db


class AssemblyType(db.Model):
    __tablename__ = "assemblyTypes"

    id = db.Column(db.Integer, primary_key=True)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Assembly type {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
        }
