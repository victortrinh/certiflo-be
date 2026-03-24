from .. import db


class Tanker(db.Model):
    __tablename__ = "tankers"

    id = db.Column(db.Integer, primary_key=True)
    tankerTypeId = db.Column(db.Integer, db.ForeignKey('tankerTypes.id', ondelete='CASCADE'))
    unitId = db.Column(db.String(255), unique=False)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    image = db.Column(db.String(255), unique=False)
    kilometers = db.Column(db.Integer, unique=False)
    engineEn = db.Column(db.String(255), unique=False)
    engineFr = db.Column(db.String(255), unique=False)
    manufacturer = db.Column(db.String(255), unique=False)
    year = db.Column(db.String, unique=False)
    capacityInLitres = db.Column(db.String, unique=False)
    capacity = db.Column(db.String(255), unique=False)
    material = db.Column(db.String(255), unique=False)
    noCompartments = db.Column(db.String, unique=False)
    price = db.Column(db.String(255), unique=False)
    dispenser = db.Column(db.String(255), unique=False)
    availability = db.Column(db.String(255), unique=False)
    cylinderRefill = db.Column(db.String(255), unique=False)
    pump = db.Column(db.String(255), unique=False)
    additionalInformationEn = db.Column(db.Text, unique=False)
    additionalInformationFr = db.Column(db.Text, unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    isCertipropane = db.Column(
        db.Boolean, server_default='f', default=False, nullable=True)

    def __repr__(self):
        return '<Tanker {}>'.format(self.unitId)

    def serialize(self):
        return {
            'id': self.id,
            'tankerTypeId': self.tankerTypeId,
            'unitId': self.unitId,
            'nameFr': self.nameFr,
            'nameEn': self.nameEn,
            'image': self.image,
            'kilometers': self.kilometers,
            'engineEn': self.engineEn,
            'engineFr': self.engineFr,
            'manufacturer': self.manufacturer,
            'year': self.year,
            'capacityInLitres': self.capacityInLitres,
            'capacity': self.capacity,
            'material': self.material,
            'noCompartments': self.noCompartments,
            'price': self.price,
            'dispenser': self.dispenser,
            'availability': self.availability,
            'cylinderRefill': self.cylinderRefill,
            'pump': self.pump,
            'additionalInformationFr': self.additionalInformationFr,
            'additionalInformationEn': self.additionalInformationEn,
            'displayOrder': self.displayOrder,
            'isCertipropane': self.isCertipropane
        }
