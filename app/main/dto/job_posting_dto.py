from flask_restx import Namespace, fields


class JobPostingDTO:
    api = Namespace('JobPosting', description='Job posting related operations')
    jobPosting = api.model('Job Posting', {
        'jobTitleFr': fields.String(required=True, description='Job title in french'),
        'jobTitleEn': fields.String(required=True, description='Job title in english'),
        'jobSummaryFr': fields.String(required=True, description='Job description in french'),
        'jobSummaryEn': fields.String(required=True, description='Job description in english'),
        'companyDescriptionFr': fields.String(required=True, description='Company description in french'),
        'companyDescriptionEn': fields.String(required=True, description='Company description in english'),
        'jobDescriptionFr': fields.String(required=True, description='Job description in french'),
        'jobDescriptionEn': fields.String(required=True, description='Job description in english'),
        'locationId': fields.Integer(required=True, description='Location'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    full_job_posting = api.model('Full Job Posting', {
        'id': fields.Integer(required=True, description='Id'),
        'jobTitleFr': fields.String(required=True, description='Job title in french'),
        'jobTitleEn': fields.String(required=True, description='Job title in english'),
        'jobSummaryFr': fields.String(required=True, description='Job description in french'),
        'jobSummaryEn': fields.String(required=True, description='Job description in english'),
        'companyDescriptionFr': fields.String(required=True, description='Company description in french'),
        'companyDescriptionEn': fields.String(required=True, description='Company description in english'),
        'jobDescriptionFr': fields.String(required=True, description='Job description in french'),
        'jobDescriptionEn': fields.String(required=True, description='Job description in english'),
        'locationId': fields.Integer(required=True, description='Location'),
        'displayOrder': fields.Integer(required=False, description='Display Order')
    })
    job_posting_id = api.model('Job Posting id', {
        'id': fields.Integer(required=True, description='The id'),
    })
