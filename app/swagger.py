from flask_restx import Api, Resource, fields
from flask import Blueprint
from .models import db, Carrier, ProduceItem, Load, Customer

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/', title='TMS API', version='1.0', description='A simple TMS API')

ns_carrier = api.namespace('carriers', description='Carrier operations')
ns_produce_item = api.namespace('produce_items', description='Produce Item operations')
ns_load = api.namespace('loads', description='Load operations')
ns_customer = api.namespace('customers', description='Customer operations')

# Models
produce_item_model = api.model('ProduceItem', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a produce item'),
    'name': fields.String(required=True, description='Produce item name'),
    'unit': fields.String(required=True, description='Unit of measurement'),
    'category': fields.String(required=True, description='Category of the produce item')
})

carrier_model = api.model('Carrier', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a carrier'),
    'name': fields.String(required=True, description='Carrier name'),
    'email': fields.String(required=True, description='Carrier email'),
    'phone': fields.String(required=True, description='Carrier phone'),
    'company': fields.String(required=True, description='Carrier company'),
    'address': fields.String(required=True, description='Carrier address'),
    'max_load_quantity': fields.Integer(required=True, description='Maximum load quantity'),
    'allowed_items': fields.List(fields.String, description='List of allowed items')
})

load_model = api.model('Load', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a load'),
    'customer_id': fields.Integer(required=True, description='ID of the customer'),
    'status': fields.String(required=True, description='Status of the load'),
    'carrier_id': fields.Integer(description='ID of the carrier'),
    'produce_items': fields.List(fields.Nested(produce_item_model), description='List of produce items')
})

customer_model = api.model('Customer', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a customer'),
    'name': fields.String(required=True, description='Customer name'),
    'pending_loads': fields.Integer(description='Number of pending loads'),
    'in_transit_loads': fields.Integer(description='Number of loads in transit')
})

# Endpoints
@ns_carrier.route('/')
class CarrierList(Resource):
    @ns_carrier.marshal_list_with(carrier_model)
    def get(self):
        """List all carriers"""
        return Carrier.query.all()

    @ns_carrier.expect(carrier_model)
    @ns_carrier.marshal_with(carrier_model, code=201)
    def post(self):
        """Create a new carrier"""
        data = api.payload
        new_carrier = Carrier(**data)
        db.session.add(new_carrier)
        db.session.commit()
        return new_carrier, 201

@ns_carrier.route('/<int:id>')
@ns_carrier.response(404, 'Carrier not found')
@ns_carrier.param('id', 'The carrier identifier')
class Carrier(Resource):
    @ns_carrier.marshal_with(carrier_model)
    def get(self, id):
        """Fetch a carrier given its identifier"""
        carrier = Carrier.query.get_or_404(id)
        return carrier

    @ns_carrier.expect(carrier_model)
    @ns_carrier.marshal_with(carrier_model)
    def put(self, id):
        """Update a carrier given its identifier"""
        data = api.payload
        carrier = Carrier.query.get_or_404(id)
        for key, value in data.items():
            setattr(carrier, key, value)
        db.session.commit()
        return carrier

    @ns_carrier.response(204, 'Carrier deleted')
    def delete(self, id):
        """Delete a carrier given its identifier"""
        carrier = Carrier.query.get_or_404(id)
        db.session.delete(carrier)
        db.session.commit()
        return '', 204

# Similar endpoints for ProduceItem, Load, and Customer...

@ns_produce_item.route('/')
class ProduceItemList(Resource):
    @ns_produce_item.marshal_list_with(produce_item_model)
    def get(self):
        """List all produce items"""
        return ProduceItem.query.all()

    @ns_produce_item.expect(produce_item_model)
    @ns_produce_item.marshal_with(produce_item_model, code=201)
    def post(self):
        """Create a new produce item"""
        data = api.payload
        new_produce_item = ProduceItem(**data)
        db.session.add(new_produce_item)
        db.session.commit()
        return new_produce_item, 201

@ns_produce_item.route('/<int:id>')
@ns_produce_item.response(404, 'ProduceItem not found')
@ns_produce_item.param('id', 'The produce item identifier')
class ProduceItem(Resource):
    @ns_produce_item.marshal_with(produce_item_model)
    def get(self, id):
        """Fetch a produce item given its identifier"""
        produce_item = ProduceItem.query.get_or_404(id)
        return produce_item

    @ns_produce_item.expect(produce_item_model)
    @ns_produce_item.marshal_with(produce_item_model)
    def put(self, id):
        """Update a produce item given its identifier"""
        data = api.payload
        produce_item = ProduceItem.query.get_or_404(id)
        for key, value in data.items():
            setattr(produce_item, key, value)
        db.session.commit()
        return produce_item

    @ns_produce_item.response(204, 'ProduceItem deleted')
    def delete(self, id):
        """Delete a produce item given its identifier"""
        produce_item = ProduceItem.query.get_or_404(id)
        db.session.delete(produce_item)
        db.session.commit()
        return '', 204

@ns_load.route('/')
class LoadList(Resource):
    @ns_load.marshal_list_with(load_model)
    def get(self):
        """List all loads"""
        return Load.query.all()

    @ns_load.expect(load_model)
    @ns_load.marshal_with(load_model, code=201)
    def post(self):
        """Create a new load"""
        data = api.payload
        new_load = Load(**data)
        db.session.add(new_load)
        db.session.commit()
        return new_load, 201

@ns_load.route('/<int:id>')
@ns_load.response(404, 'Load not found')
@ns_load.param('id', 'The load identifier')
class Load(Resource):
    @ns_load.marshal_with(load_model)
    def get(self, id):
        """Fetch a load given its identifier"""
        load = Load.query.get_or_404(id)
        return load

    @ns_load.expect(load_model)
    @ns_load.marshal_with(load_model)
    def put(self, id):
        """Update a load given its identifier"""
        data = api.payload
        load = Load.query.get_or_404(id)
        for key, value in data.items():
            setattr(load, key, value)
        db.session.commit()
        return load

    @ns_load.response(204, 'Load deleted')
    def delete(self, id):
        """Delete a load given its identifier"""
        load = Load.query.get_or_404(id)
        db.session.delete(load)
        db.session.commit()
        return '', 204

@ns_customer.route('/')
class CustomerList(Resource):
    @ns_customer.marshal_list_with(customer_model)
    def get(self):
        """List all customers"""
        return Customer.query.all()

    @ns_customer.expect(customer_model)
    @ns_customer.marshal_with(customer_model, code=201)
    def post(self):
        """Create a new customer"""
        data = api.payload
        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer, 201

@ns_customer.route('/<int:id>')
@ns_customer.response(404, 'Customer not found')
@ns_customer.param('id', 'The customer identifier')
class Customer(Resource):
    @ns_customer.marshal_with(customer_model)
    def get(self, id):
        """Fetch a customer given its identifier"""
        customer = Customer.query.get_or_404(id)
        return customer

    @ns_customer.expect(customer_model)
    @ns_customer.marshal_with(customer_model)
    def put(self, id):
        """Update a customer given its identifier"""
        data = api.payload
        customer = Customer.query.get_or_404(id)
        for key, value in data.items():
            setattr(customer, key, value)
        db.session.commit()
        return customer

    @ns_customer.response(204, 'Customer deleted')
    def delete(self, id):
        """Delete a customer given its identifier"""
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return '', 204
