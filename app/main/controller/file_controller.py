import os

from flask_restx import Resource
from flask import request, jsonify, send_from_directory
from ..dto.file_dto import FileDTO
from ..service.auth_service import Auth
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, 'uploads')

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

auth = Auth.auth
api = FileDTO.api


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route("/")
class GetFiles(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Get files')
    def get(self):
        files = []
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        for filename in os.listdir(UPLOAD_DIRECTORY):
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)
        return jsonify(files)


@api.route("/download/<fileName>")
class Download(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Download file')
    def get(self, fileName):
        return send_from_directory(UPLOAD_DIRECTORY, fileName, as_attachment=True)


@api.route('/upload')
class Upload(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new file')
    @api.expect(upload_parser)
    def post(self):
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)

        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > MAX_FILE_SIZE:
            resp = jsonify({'message': 'File too large. Maximum size is 10 MB.'})
            resp.status_code = 413
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIRECTORY, filename))
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(
                {'message': 'Allowed file types are: pdf'})
            resp.status_code = 400
            return resp
