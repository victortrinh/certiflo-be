#import uuid
#import datetime

from flask import jsonify
from app.main import db
from app.main.model.jobPosting import JobPosting


def get_job_postings():
    job_postings = JobPosting.query.all()
    return jsonify(job_postings=[job_posting.serialize() for job_posting in job_postings])


def save_new_job_posting(data):
    new_job_posting = JobPosting(
        jobTitleFr=data['jobTitleFr'],
        jobTitleEn=data['jobTitleEn'],
        jobSummaryFr=data['jobSummaryFr'],
        jobSummaryEn=data['jobSummaryEn'],
        companyDescriptionFr=data['companyDescriptionFr'],
        companyDescriptionEn=data['companyDescriptionEn'],
        jobDescriptionFr=data['jobDescriptionFr'],
        jobDescriptionEn=data['jobDescriptionEn'],
        locationId=data['locationId']
    )
    save_changes(new_job_posting)
    response_object = {
        'id': new_job_posting.id,
    }
    return response_object, 201


def update_job_posting(data):
    query = db.session.query(JobPosting)
    query = query.filter(JobPosting.id == data['id'])
    record = query.one()
    record.jobTitleFr = data["jobTitleFr"]
    record.jobTitleEn = data["jobTitleEn"]
    record.jobSummaryFr = data["jobSummaryFr"]
    record.jobSummaryEn = data["jobSummaryEn"]
    record.companyDescriptionFr = data["companyDescriptionFr"]
    record.companyDescriptionEn = data["companyDescriptionEn"]
    record.jobDescriptionFr = data["jobDescriptionFr"]
    record.jobDescriptionEn = data["jobDescriptionEn"]
    record.locationId = data["locationId"]
    db.session.flush()
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully updated row.',
    }
    return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_job_posting(data):
    job_posting = JobPosting.query.filter_by(id=data['id']).one()
    db.session.delete(job_posting)
    db.session.commit()
    return {'message': "Job Posting id :" + str(data['id']) + " was deleted successfully"}, 200
