from .. import db


class GalleryImage(db.Model):
    __tablename__ = "galleryImages"

    id = db.Column(db.Integer, primary_key=True)
    galleryId = db.Column(db.Integer, unique=False)
    image = db.Column(db.Text, unique=False)
    displayOrder = db.Column(db.Integer, unique=False)
    isCertipropane = db.Column(
        db.Boolean, server_default='f', default=False, nullable=True)

    def __repr__(self):
        return '<GalleryImage {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'image': self.image,
            'galleryId': self.galleryId,
            'displayOrder': self.displayOrder,
            'isCertipropane': self.isCertipropane
        }
