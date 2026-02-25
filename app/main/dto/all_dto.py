from flask_restx import Namespace, fields


class AllDTO:
    api = Namespace('All', description='Get all related operations')
