from .. import db


class JobPosting(db.Model):
    __tablename__ = "jobPostings"

    id = db.Column(db.Integer, primary_key=True)
    jobTitleFr = db.Column(db.Text, unique=False)
    jobTitleEn = db.Column(db.Text, unique=False)
    jobSummaryFr = db.Column(db.Text, unique=False)
    jobSummaryEn = db.Column(db.Text, unique=False)
    companyDescriptionFr = db.Column(db.Text, unique=False)
    companyDescriptionEn = db.Column(db.Text, unique=False)
    jobDescriptionFr = db.Column(db.Text, unique=False)
    jobDescriptionEn = db.Column(db.Text, unique=False)
    locationId = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<Job postings {}>'.format(self.jobTitleEn)

    def serialize(self):
        return {
            'id': self.id,
            'jobTitleFr': self.jobTitleFr,
            'jobTitleEn': self.jobTitleEn,
            'jobSummaryFr': self.jobSummaryFr,
            'jobSummaryEn': self.jobSummaryEn,
            'companyDescriptionFr': self.companyDescriptionFr,
            'companyDescriptionEn': self.companyDescriptionEn,
            'jobDescriptionFr': self.jobDescriptionFr,
            'jobDescriptionEn': self.jobDescriptionEn,
            'locationId': self.locationId
        }
