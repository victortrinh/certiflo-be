from .. import db


class Assembly(db.Model):
    __tablename__ = "assemblies"

    id = db.Column(db.Integer, primary_key=True)
    assemblyTypeId = db.Column(db.Integer, unique=False)
    image = db.Column(db.String(255), unique=False)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    descriptionEn = db.Column(db.Text(), unique=False)
    descriptionFr = db.Column(db.Text(), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    isCertipropane = db.Column(
        db.Boolean, server_default='f', default=False, nullable=True)

    def __repr__(self):
        return '<Assembly {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'assemblyTypeId': self.assemblyTypeId,
            'image': self.image,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'descriptionEn': self.descriptionEn,
            'descriptionFr': self.descriptionFr,
            'displayOrder': self.displayOrder,
            'isCertipropane': self.isCertipropane
        }
