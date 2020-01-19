# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from flask_cors import CORS

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.resource_controller import api as resource_ns
from .main.controller.location_controller import api as location_ns
from .main.controller.telephone_controller import api as telephone_ns
from .main.controller.email_controller import api as email_ns
from .main.controller.opening_controller import api as opening_ns
from .main.controller.manufacturerImage_controller import api as manufacturerImage_ns
from .main.controller.manufacturer_controller import api as manufacturer_ns
from .main.controller.realization_controller import api as realization_ns
from .main.controller.realization_type_controller import api as realization_type_ns

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
api.add_namespace(location_ns, path=BASE_URL + '/location')
api.add_namespace(telephone_ns, path=BASE_URL + '/telephone')
api.add_namespace(email_ns, path=BASE_URL + '/email')
api.add_namespace(opening_ns, path=BASE_URL + '/opening')
api.add_namespace(manufacturerImage_ns, path=BASE_URL + "/manufacturerImage")
api.add_namespace(manufacturer_ns, path=BASE_URL + "/manufacturer")
api.add_namespace(realization_ns, path=BASE_URL + "/realization")
api.add_namespace(realization_type_ns, path=BASE_URL + "/realizationType")

CORS(api.blueprint)
