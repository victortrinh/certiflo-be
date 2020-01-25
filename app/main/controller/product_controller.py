from flask_restplus import Resource
from flask import request
from ..service.product_service import get_products, save_new_product, update_product, delete_product
from ..dto.product_dto import ProductDTO

api = ProductDTO.api


@api.route('/getAll')
class GetProducts(Resource):
    @api.doc('Get products')
    def get(self):
        return get_products()


@api.route('/save')
class SaveProduct(Resource):
    @api.doc('Save new product')
    @api.expect(ProductDTO.product, validate=True)
    def post(self):
        data = request.json
        return save_new_product(data)


@api.route('/update')
class UpdateProduct(Resource):
    @api.doc('Update the product')
    @api.expect(ProductDTO.full_product, validate=True)
    def put(self):
        data = request.json
        return update_product(data)


@api.route('/delete')
class DeleteProduct(Resource):
    @api.doc('Delete product')
    @api.expect(ProductDTO.product_id, validate=True)
    def delete(self):
        data = request.json
        return delete_product(data)
