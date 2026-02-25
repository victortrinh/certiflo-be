from flask_restx import Resource
from flask import request
from ..service.job_posting_service import get_job_postings, save_new_job_posting, delete_job_posting, update_job_postings
from ..dto.job_posting_dto import JobPostingDTO

api = JobPostingDTO.api


@api.route('/all')
class GetJobPostings(Resource):
    @api.doc('Get job postings')
    def get(self):
        return get_job_postings()


@api.route('/save')
class SaveJobPosting(Resource):
    @api.doc('Save new job posting')
    @api.expect(JobPostingDTO.jobPosting, validate=True)
    def post(self):
        data = request.json
        return save_new_job_posting(data)


@api.route('/update')
class UpdateJobPostings(Resource):
    @api.doc('Update the job posting')
    @api.expect([JobPostingDTO.full_job_posting], validate=True)
    def put(self):
        data = request.json
        return update_job_postings(data)


@api.route('/delete')
class DeleteJobPosting(Resource):
    @api.doc('Delete job posting')
    @api.expect(JobPostingDTO.job_posting_id, validate=True)
    def delete(self):
        data = request.json
        return delete_job_posting(data)
