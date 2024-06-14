from flask import Blueprint, request, jsonify
from . import db
from .models import Carrier, ProduceItem, Load

main_bp = Blueprint('main', __name__)

@main_bp.route('/carriers', methods=['POST'])
def create_carrier():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    company = data.get('company')
    address = data.get('address')
    max_load_quantity = data.get('max_load_quantity')
    allowed_items = data.get('allowed_items')

    if not all([name, email, phone, company, address, max_load_quantity]):
        return jsonify({"error": "Missing required fields"}), 400

    carrier = Carrier(
        name=name,
        email=email,
        phone=phone,
        company=company,
        address=address,
        max_load_quantity=max_load_quantity,
        allowed_items=allowed_items
    )
    db.session.add(carrier)
    db.session.commit()
    return jsonify(carrier.as_dict()), 201

@main_bp.route('/carriers', methods=['GET'])
def get_carriers():
    carriers = Carrier.query.all()
    return jsonify([carrier.as_dict() for carrier in carriers]), 200

@main_bp.route('/carriers/<int:id>', methods=['GET'])
def get_carrier(id):
    carrier = Carrier.query.get(id)
    if carrier is None:
        return jsonify({"error": "Carrier not found"}), 404
    return jsonify(carrier.as_dict()), 200

@main_bp.route('/carriers/<int:carrier_id>', methods=['PUT'])
def update_carrier(carrier_id):
    data = request.get_json()
    carrier = Carrier.query.get_or_404(carrier_id)
    carrier.name = data['name']
    carrier.email = data['email']
    carrier.phone = data['phone']
    carrier.company = data['company']
    carrier.address = data['address']
    carrier.max_load_quantity = data['max_load_quantity']
    carrier.allowed_items = data.get('allowed_items', [])
    db.session.commit()
    return jsonify({"message": "Carrier updated successfully"}), 200


@main_bp.route('/carriers/<int:carrier_id>', methods=['DELETE'])
def delete_carrier(carrier_id):
    carrier = Carrier.query.get_or_404(carrier_id)
    db.session.delete(carrier)
    db.session.commit()
    return jsonify({"message": "Carrier deleted successfully"}), 200


@main_bp.route('/produce_items', methods=['POST'])
def create_produce_item():
    data = request.get_json()
    new_produce_item = ProduceItem(
        name=data['name'],
        unit=data['unit'],
        category=data['category']
    )
    db.session.add(new_produce_item)
    db.session.commit()
    return jsonify({"message": "Produce item created successfully"}), 201


@main_bp.route('/produce_items', methods=['GET'])
def get_produce_items():
    produce_items = ProduceItem.query.all()
    return jsonify([produce_item.as_dict() for produce_item in produce_items]), 200


@main_bp.route('/produce_items/<int:produce_item_id>', methods=['GET'])
def get_produce_item(produce_item_id):
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    return jsonify(produce_item.as_dict()), 200


@main_bp.route('/produce_items/<int:produce_item_id>', methods=['PUT'])
def update_produce_item(produce_item_id):
    data = request.get_json()
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    produce_item.name = data['name']
    produce_item.unit = data['unit']
    produce_item.category = data['category']
    db.session.commit()
    return jsonify({"message": "Produce item updated successfully"}), 200


@main_bp.route('/produce_items/<int:produce_item_id>', methods=['DELETE'])
def delete_produce_item(produce_item_id):
    produce_item = ProduceItem.query.get_or_404(produce_item_id)
    db.session.delete(produce_item)
    db.session.commit()
    return jsonify({"message": "Produce item deleted successfully"}), 200


@main_bp.route('/loads', methods=['POST'])
def create_load():
    data = request.get_json()
    if not data or not data.get('customer'):
        return jsonify({"error": "Customer field is required"}), 400

    load = Load(customer=data['customer'])
    # load = Load(customer_id=data['customer_id'], status=data.get('status', 'pending'))
    db.session.add(load)
    db.session.commit()
    return jsonify(load.as_dict()), 201


@main_bp.route('/loads', methods=['GET'])
def get_loads():
    loads = Load.query.all()
    return jsonify([load.as_dict() for load in loads]), 200


@main_bp.route('/loads/<int:load_id>', methods=['GET'])
def get_load(load_id):
    load = Load.query.get_or_404(load_id)
    return jsonify(load.as_dict()), 200


@main_bp.route('/loads/<int:load_id>', methods=['PUT'])
def update_load(load_id):
    data = request.get_json()
    load = Load.query.get_or_404(load_id)
    load.customer = data['customer']
    # load.customer_id = data['customer_id']

    load.carrier_id = data.get('carrier_id', None)
    db.session.commit()
    return jsonify({"message": "Load updated successfully"}), 200


@main_bp.route('/loads/<int:load_id>', methods=['DELETE'])
def delete_load(load_id):
    load = Load.query.get_or_404(load_id)
    db.session.delete(load)
    db.session.commit()
    return jsonify({"message": "Load deleted successfully"}), 200

# # Customer Routes
# @main_bp.route('/customers', methods=['POST'])
# def create_customer():
#     data = request.get_json()
#     new_customer = Customer(
#         name=data['name'],
#         address=data['address'],
#         email=data['email'],
#         phone=data['phone']
#     )
#     db.session.add(new_customer)
#     db.session.commit()
#     return jsonify({"message": "Customer created successfully"}), 201
#
# @main_bp.route('/customers', methods=['GET'])
# def get_customers():
#     customers = Customer.query.all()
#     return jsonify([customer.as_dict() for customer in customers]), 200
#
# @main_bp.route('/customers/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     return jsonify(customer.as_dict()), 200
#
# @main_bp.route('/customers/<int:customer_id>', methods=['PUT'])
# def update_customer(customer_id):
#     data = request.get_json()
#     customer = Customer.query.get_or_404(customer_id)
#     customer.name = data['name']
#     customer.address = data['address']
#     customer.email = data['email']
#     customer.phone = data['phone']
#     db.session.commit()
#     return jsonify({"message": "Customer updated successfully"}), 200
#
# @main_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
# def delete_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     db.session.delete(customer)
#     db.session.commit()
#     return jsonify({"message": "Customer deleted successfully"}), 200