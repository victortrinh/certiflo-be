from flask_restplus import Resource
from flask import request
from ..service.email_service import get_emails, save_new_email, update_email, delete_email
from ..dto.email_dto import EmailDTO

api = EmailDTO.api


@api.route('/getAll')
class GetEmailsByLocationId(Resource):
    @api.doc('Get emails')
    def get(self):
        return get_emails()


@api.route('/save')
class SaveEmail(Resource):
    @api.doc('Save new email')
    @api.expect(EmailDTO.email, validate=True)
    def post(self):
        data = request.json
        return save_new_email(data)


@api.route('/update')
class UpdateEmail(Resource):
    @api.doc('Update the email')
    @api.expect(EmailDTO.full_email, validate=True)
    def put(self):
        data = request.json
        return update_email(data)


@api.route('/delete')
class DeleteEmail(Resource):
    @api.doc('Delete email')
    @api.expect(EmailDTO.email_id, validate=True)
    def delete(self):
        data = request.json
        return delete_email(data)
