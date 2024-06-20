from flask import Blueprint, request, jsonify
from . import db
from .models import Carrier, ProduceItem, Load, Customer, ValidationError

main_bp = Blueprint('main', __name__)

@main_bp.route('/loads', methods=['POST'])
def create_load():
    data = request.get_json()
    if not data or not all(key in data for key in ['status', 'customer_id']):
        return jsonify({'message': 'Invalid input'}), 400
    try:
        load = Load.create_load(status=data['status'], customer_id=data['customer_id'])
        return jsonify({'message': 'Load created successfully', 'load': load.id}), 201
    except ValidationError as e:
        return jsonify({'message': str(e)}), 400

@main_bp.route('/loads/<int:load_id>', methods=['GET'])
def get_load(load_id):
    load = Load.query.get_or_404(load_id)
    return jsonify({'id': load.id, 'status': load.status, 'customer_id': load.customer_id, 'carrier_id': load.carrier_id})

@main_bp.route('/loads', methods=['GET'])
def get_loads():
    loads = Load.query.all()
    return jsonify([{'id': load.id, 'status': load.status, 'customer_id': load.customer_id, 'carrier_id': load.carrier_id} for load in loads])

@main_bp.route('/loads/<int:load_id>', methods=['PUT'])
def update_load(load_id):
    load = Load.query.get_or_404(load_id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid input'}), 400
    load.status = data.get('status', load.status)
    load.customer_id = data.get('customer_id', load.customer_id)
    db.session.commit()
    return jsonify({'message': 'Load updated successfully'})

@main_bp.route('/loads/<int:load_id>', methods=['DELETE'])
def delete_load(load_id):
    load = Load.query.get_or_404(load_id)
    db.session.delete(load)
    db.session.commit()
    return jsonify({'message': 'Load deleted successfully'})

# customer CRUD
@main_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully', 'customer': customer.id}), 201

@main_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({'id': customer.id, 'name': customer.name})

@main_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': customer.id, 'name': customer.name} for customer in customers])

@main_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@main_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# carrier CRUD
@main_bp.route('/carriers', methods=['POST'])
def create_carrier():
    data = request.get_json()
    carrier = Carrier(name=data['name'], address=data['address'], email=data['email'], phone=data['phone'], company=data['company'], allowed_items=data['allowed_items'], max_load_quantity=data['max_load_quantity'])
    db.session.add(carrier)
    db.session.commit()
    return jsonify({'message': 'Carrier created successfully', 'carrier': carrier.id}), 201

@main_bp.route('/carriers/<int:carrier_id>', methods=['GET'])
def get_carrier(carrier_id):
    carrier = Carrier.query.get_or_404(carrier_id)
    return jsonify({'id': carrier.id, 'name': carrier.name, 'address': carrier.address, 'email': carrier.email, 'phone': carrier.phone, 'company': carrier.company, 'allowed_items': carrier.allowed_items, 'max_load_quantity': carrier.max_load_quantity})

@main_bp.route('/carriers', methods=['GET'])
def get_carriers():
    carriers = Carrier.query.all()
    return jsonify([{'id': carrier.id, 'name': carrier.name, 'address': carrier.address, 'email': carrier.email, 'phone': carrier.phone, 'company': carrier.company, 'allowed_items': carrier.allowed_items, 'max_load_quantity': carrier.max_load_quantity} for carrier in carriers])

@main_bp.route('/carriers/<int:carrier_id>', methods=['PUT'])
def update_carrier(carrier_id):
    carrier = Carrier.query.get_or_404(carrier_id)
    data = request.get_json()
    carrier.name = data.get('name', carrier.name)
    carrier.address = data.get('address', carrier.address)
    carrier.email = data.get('email', carrier.email)
    carrier.phone = data.get('phone', carrier.phone)
    carrier.company = data.get('company', carrier.company)
    carrier.allowed_items = data.get('allowed_items', carrier.allowed_items)
    carrier.max_load_quantity = data.get('max_load_quantity', carrier.max_load_quantity)
    db.session.commit()
    return jsonify({'message': 'Carrier updated successfully'})

@main_bp.route('/carriers/<int:carrier_id>', methods=['DELETE'])
def delete_carrier(carrier_id):
    carrier = Carrier.query.get_or_404(carrier_id)
    db.session.delete(carrier)
    db.session.commit()
    return jsonify({'message': 'Carrier deleted successfully'})

#ProduceItem carrier
@main_bp.route('/produce_items', methods=['POST'])
def create_produce_item():
    data = request.get_json()
    produce_item = ProduceItem(name=data['name'])
    db.session.add(produce_item)
    db.session.commit()
    return jsonify({'message': 'Produce item created successfully', 'produce_item': produce_item.id}), 201

@main_bp.route('/produce_items/<int:produce_item_id>', methods=['GET'])
def get_produce_item(produce_item_id):
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    return jsonify({'id': produce_item.id, 'name': produce_item.name})

@main_bp.route('/produce_items', methods=['GET'])
def get_produce_items():
    produce_items = ProduceItem.query.all()
    return jsonify([{'id': produce_item.id, 'name': produce_item.name} for produce_item in produce_items])

@main_bp.route('/produce_items/<int:produce_item_id>', methods=['PUT'])
def update_produce_item(produce_item_id):
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    data = request.get_json()
    produce_item.name = data.get('name', produce_item.name)
    db.session.commit()
    return jsonify({'message': 'Produce item updated successfully'})

@main_bp.route('/produce_items/<int:produce_item_id>', methods=['DELETE'])
def delete_produce_item(produce_item_id):
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    db.session.delete(produce_item)
    db.session.commit()
    return jsonify({'message': 'Produce item deleted successfully'})

def init_app(app):
    app.register_blueprint(main_bp)
