from flask import Blueprint, request, jsonify
from config import db
from models import Customer 

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201
