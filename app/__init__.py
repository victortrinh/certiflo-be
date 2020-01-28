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
from .main.controller.product_controller import api as product_ns
from .main.controller.manufacturer_image_controller import api as manufacturer_image_ns
from .main.controller.manufacturer_controller import api as manufacturer_ns
from .main.controller.realization_controller import api as realization_ns
from .main.controller.realization_type_controller import api as realization_type_ns
from .main.controller.employee_controller import api as employee_ns
from .main.controller.tanker_type_controller import api as tanker_type_ns
from .main.controller.assembly_controller import api as assembly_ns
from .main.controller.assembly_type_controller import api as assembly_type_ns
from .main.controller.tanker_controller import api as tanker_ns
from .main.controller.gallery_image_controller import api as gallery_image_ns
from .main.controller.gallery_controller import api as gallery_ns
from .main.controller.job_posting_controller import api as job_posting_ns

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
api.add_namespace(product_ns, path=BASE_URL + '/product')
api.add_namespace(manufacturer_image_ns, path=BASE_URL + "/manufacturerImage")
api.add_namespace(manufacturer_ns, path=BASE_URL + "/manufacturer")
api.add_namespace(realization_ns, path=BASE_URL + "/realization")
api.add_namespace(realization_type_ns, path=BASE_URL + "/realizationType")
api.add_namespace(employee_ns, path=BASE_URL + "/employee")
api.add_namespace(tanker_type_ns, path=BASE_URL + "/tankerType")
api.add_namespace(assembly_ns, path=BASE_URL + '/assembly')
api.add_namespace(assembly_type_ns, path=BASE_URL + '/assemblyType')
api.add_namespace(tanker_ns, path=BASE_URL + "/tanker")
api.add_namespace(gallery_image_ns, path=BASE_URL + "/galleryImage")
api.add_namespace(gallery_ns, path=BASE_URL + "/gallery")
api.add_namespace(job_posting_ns, path=BASE_URL + "/jobPosting")

CORS(api.blueprint)
