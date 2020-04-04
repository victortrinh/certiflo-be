from flask_restplus import Namespace, fields


class AllDTO:
    api = Namespace('All', description='Get all related operations')
