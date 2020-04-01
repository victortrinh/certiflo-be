from flask_restplus import Resource
from flask import request
from ..service.employee_service import get_employees, save_new_employee, update_employee, delete_employee
from ..dto.employee_dto import EmployeeDTO
from ..service.auth_service import Auth
from flask_httpauth import HTTPTokenAuth

api = EmployeeDTO.api
auth = Auth.auth


@api.route('/all')
class GetEmployees(Resource):
    @api.doc('Get all employees')
    def get(self):
        return get_employees()


@api.route('/save')
class SaveEmployee(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Save new employee')
    @api.expect(EmployeeDTO.employee, validate=True)
    def post(self):
        data = request.json
        return save_new_employee(data)


@api.route('/update')
class UpdateEmployee(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Update an employee')
    @api.expect(EmployeeDTO.full_employee, validate=True)
    def put(self):
        data = request.json
        return update_employee(data)


@api.route('/delete')
class DeleteEmployee(Resource):
    @auth.login_required
    @api.doc(security='Bearer')
    @api.doc('Delete employee')
    @api.expect(EmployeeDTO.employee_id, validate=True)
    def delete(self):
        data = request.json
        return delete_employee(data)
