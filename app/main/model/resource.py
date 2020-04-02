from .. import db


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), unique=False)
    page = db.Column(db.String(255), unique=False)
    object_key = db.Column(db.String(255), unique=False)
    resource = db.Column(db.Text, unique=False)
    isHtml = db.Column(
        db.Boolean, server_default='f', default=False, nullable=True)

    def __repr__(self):
        return '<Resource {}>'.format(self.resource)

    def serialize(self):
        return {
            'id': self.id,
            'language': self.language,
            'page': self.page,
            'object_key': self.object_key,
            'resource': self.resource,
            'isHtml': self.isHtml
        }
