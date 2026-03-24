from .. import db


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    nameEn = db.Column(db.String(255), unique=False)
    nameFr = db.Column(db.String(255), unique=False)
    address = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    emails = db.relationship('Email', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    openings = db.relationship('Opening', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    telephones = db.relationship('Telephone', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)
    job_postings = db.relationship('JobPosting', backref='location', cascade='all, delete-orphan', passive_deletes=True, lazy=True)

    def __repr__(self):
        return '<Location {}>'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'nameEn': self.nameEn,
            'nameFr': self.nameFr,
            'address': self.address,
            'displayOrder': self.displayOrder
        }
