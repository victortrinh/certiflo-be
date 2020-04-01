from .. import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), unique=False)
    lastName = db.Column(db.String(255), unique=False)
    roleFr = db.Column(db.String(255), unique=False)
    roleEn = db.Column(db.String(255), unique=False)
    email = db.Column(db.String(255), unique=False)
    company = db.Column(db.String(255), unique=False)
    image = db.Column(db.String(255), unique=False)
    descriptionEn = db.Column(db.Text, unique=False)
    descriptionFr = db.Column(db.Text, unique=False)
    displayOrder = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Employee {}>'.format(self.description)

    def serialize(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'roleFr': self.roleFr,
            'roleEn': self.roleEn,
            'email': self.email,
            'company': self.company,
            'image': self.image,
            'descriptionEn': self.descriptionEn,
            'descriptionFr': self.descriptionFr,
            'displayOrder': self.displayOrder
        }
