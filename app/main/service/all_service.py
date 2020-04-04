from flask import jsonify
from app.main.model.assembly import Assembly
from app.main.model.assemblyType import AssemblyType
from app.main.model.email import Email
from app.main.model.employee import Employee
from app.main.model.galleryImage import GalleryImage
from app.main.model.gallery import Gallery
from app.main.model.jobPosting import JobPosting
from app.main.model.location import Location
from app.main.model.manufacturer import Manufacturer
from app.main.model.manufacturerImage import ManufacturerImage
from app.main.model.opening import Opening
from app.main.model.product import Product
from app.main.model.realization import Realization
from app.main.model.realizationType import RealizationType
from app.main.model.resource import Resource
from app.main.model.tanker import Tanker
from app.main.model.tankerType import TankerType
from app.main.model.telephone import Telephone


def get_all():
    assemblies = Assembly.query.all()
    assemblyTypes = AssemblyType.query.all()
    emails = Email.query.all()
    employees = Employee.query.all()
    galleryImages = GalleryImage.query.all()
    galleries = Gallery.query.all()
    job_postings = JobPosting.query.all()
    locations = Location.query.all()
    manufacturers = Manufacturer.query.all()
    manufacturerImages = ManufacturerImage.query.all()
    openings = Opening.query.all()
    products = Product.query.all()
    realizations = Realization.query.all()
    realizationTypes = RealizationType.query.all()
    resources = Resource.query.all()
    tankers = Tanker.query.all()
    tankerTypes = TankerType.query.all()
    telephones = Telephone.query.all()
    return jsonify(assemblies=[assembly.serialize() for assembly in assemblies],
                   assemblyTypes=[assemblyType.serialize()
                                  for assemblyType in assemblyTypes],
                   emails=[email.serialize() for email in emails],
                   employees=[employee.serialize() for employee in employees],
                   galleryImages=[galleryImage.serialize()
                                  for galleryImage in galleryImages],
                   galleries=[gallery.serialize() for gallery in galleries],
                   job_postings=[job_posting.serialize()
                                 for job_posting in job_postings],
                   locations=[location.serialize() for location in locations],
                   manufacturers=[manufacturer.serialize()
                                  for manufacturer in manufacturers],
                   manufacturerImages=[manufacturerImage.serialize(
                   ) for manufacturerImage in manufacturerImages],
                   openings=[opening.serialize() for opening in openings],
                   products=[product.serialize() for product in products],
                   realizations=[realization.serialize()
                                 for realization in realizations],
                   realizationTypes=[realizationType.serialize()
                                     for realizationType in realizationTypes],
                   resources=[resource.serialize() for resource in resources],
                   tankers=[tanker.serialize() for tanker in tankers],
                   tankerTypes=[tankerType.serialize()
                                for tankerType in tankerTypes],
                   telephones=[telephone.serialize() for telephone in telephones])
