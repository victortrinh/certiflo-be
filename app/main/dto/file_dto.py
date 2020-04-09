from flask_restplus import Namespace, fields


class FileDTO:
    api = Namespace('File', description='Get file related operations')
    fileName = api.model('File name', {
        'fileName': fields.String(required=True, description='File name'),
    })
