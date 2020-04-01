from flask_restplus import Namespace, fields


class TankerDTO:
    api = Namespace('Tanker', description='Tanker related operations')
    tanker = api.model('Tanker', {
        'tankerTypeId': fields.Integer(required=True, description='The tanker type Id'),
        'nameEn': fields.String(required=False, description='Tanker name in english'),
        'nameFr': fields.String(required=False, description='Tanker name in french'),
        'unitId': fields.String(required=True, description='Tanker unit Id'),
        'image': fields.String(required=False, description='Tanker image'),
        'kilometers': fields.Integer(required=False, description='Tanker number of kilometers'),
        'engineEn': fields.String(required=False, description='Tanker engine in english'),
        'engineFr': fields.String(required=False, description='Tanker engine in french'),
        'manufacturer': fields.String(required=False, description='Tanker manufacturer'),
        'year': fields.Integer(required=False, description='Tanker production year'),
        'capacityInLitres': fields.Integer(required=False, description='Tanker fuel capacity in liters'),
        'capacity': fields.String(required=False, description='Tanker additional capacity information'),
        'material': fields.String(required=False, description='Tanker material'),
        'noCompartments': fields.Integer(required=False, description='Tanker number of compartments'),
        'price': fields.String(required=False, description='Tanker price'),
        'dispenser': fields.String(required=False, description='Tank dispenser'),
        'availability': fields.String(required=False, description='Tank availability'),
        'cylinderRefill': fields.String(required=False, description='Tank cylinderRefill'),
        'pump': fields.String(required=False, description='Tank pump'),
        'additionalInformationEn': fields.String(required=False, description='Tank additional information in english'),
        'additionalInformationFr': fields.String(required=False, description='Tank additional information in french'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    full_tanker = api.model('Full tanker', {
        'id': fields.Integer(required=True, description='The tanker id'),
        'nameEn': fields.String(required=False, description='Tanker name in english'),
        'nameFr': fields.String(required=False, description='Tanker name in french'),
        'unitId': fields.String(required=True, description='Tanker unit Id'),
        'image': fields.String(required=False, description='Tanker image'),
        'kilometers': fields.Integer(required=False, description='Tanker number of kilometers'),
        'engineEn': fields.String(required=False, description='Tanker engine in english'),
        'engineFr': fields.String(required=False, description='Tanker engine in french'),
        'manufacturer': fields.String(required=False, description='Tanker manufacturer'),
        'year': fields.Integer(required=False, description='Tanker production year'),
        'capacityInLitres': fields.Integer(required=False, description='Tanker fuel capacity in liters'),
        'capacity': fields.String(required=False, description='Tanker additional capacity information'),
        'material': fields.String(required=False, description='Tanker material'),
        'noCompartments': fields.Integer(required=False, description='Tanker number of compartments'),
        'price': fields.String(required=False, description='Tanker price'),
        'dispenser': fields.String(required=False, description='Tank dispenser'),
        'availability': fields.String(required=False, description='Tank availability'),
        'cylinderRefill': fields.String(required=False, description='Tank cylinderRefill'),
        'pump': fields.String(required=False, description='Tank pump'),
        'additionalInformationEn': fields.String(required=False, description='Tank additional information in english'),
        'additionalInformationFr': fields.String(required=False, description='Tank additional information in french'),
        'displayOrder': fields.String(required=True, description='Display Order')
    })
    tanker_id = api.model('Tanker id', {
        'id': fields.Integer(required=True, description='The Tanker id'),
    })
