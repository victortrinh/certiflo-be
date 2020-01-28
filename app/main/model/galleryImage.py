from .. import db


class GalleryImage(db.Model):
    __tablename__ = "galleryImages"

    id = db.Column(db.Integer, primary_key=True)
    galleryId = db.Column(db.Integer, unique=False)
    image = db.Column(db.Text, unique=False)

    def __repr__(self):
        return '<GalleryImage {}>'.format(self.nameEn)

    def serialize(self):
        return {
            'id': self.id,
            'image': self.image,
            'galleryId': self.galleryId
        }
