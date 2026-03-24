from flask_restx import Resource
from flask import request
from ..service.email_service import get_emails, save_new_email, delete_email, update_emails
from ..dto.email_dto import EmailDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = EmailDTO.api
auth = Auth.auth


@api.route('/all')
class GetEmailsByLocationId(Resource):
    @api.doc('Get emails')
    def get(self):
        return get_emails()


@api.route('/save')
class SaveEmail(Resource):
    @api.doc('Save new email')
    @auth.login_required
    @api.doc(security='Bearer')
    @api.expect(EmailDTO.email, validate=True)
    def post(self):
        data = request.json
        return save_new_email(data)


@api.route('/update')
class UpdateEmails(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update the email')
    @api.expect([EmailDTO.full_email], validate=True)
    def put(self):
        data = request.json
        return update_emails(data)


@api.route('/delete')
class DeleteEmail(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete email')
    @api.expect(EmailDTO.email_id, validate=True)
    def delete(self):
        data = request.json
        return delete_email(data)
