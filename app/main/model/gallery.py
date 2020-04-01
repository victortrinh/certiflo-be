from .. import db


class Gallery(db.Model):
    __tablename__ = "galleries"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Gallery {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'company': self.company,
            'displayOrder': self.displayOrder
        }
