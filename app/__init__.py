# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from flask_cors import CORS

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.resource_controller import api as resource_ns

BASE_URL = '/api'

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Certiflo',
          version='1.0',
          description='All servicing for certiflo'
          )

api.blueprint.after_request


def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')


api.add_namespace(user_ns, path=BASE_URL + '/user')
api.add_namespace(auth_ns, path=BASE_URL + '/auth')
api.add_namespace(resource_ns, path=BASE_URL + '/resource')

CORS(api.blueprint)
