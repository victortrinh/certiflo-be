from .. import db


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), unique=False)
    page = db.Column(db.String(255), unique=False)
    object_key = db.Column(db.String(255), unique=False)
    resource = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Resource {}>'.format(self.resource)

    def serialize(self):
        return {
            'id': self.id,
            'language': self.language,
            'page': self.page,
            'object_key': self.object_key,
            'resource': self.resource
        }
