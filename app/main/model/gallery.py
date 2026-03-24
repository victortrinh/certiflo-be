from .. import db


class Gallery(db.Model):
    __tablename__ = "galleries"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    images = db.relationship('GalleryImage', backref='gallery', cascade='all, delete-orphan', passive_deletes=True, lazy=True)

    def __repr__(self):
        return '<Gallery {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'company': self.company,
            'displayOrder': self.displayOrder
        }
