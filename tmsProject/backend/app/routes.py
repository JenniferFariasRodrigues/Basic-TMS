from flask import request, jsonify
from app import app, db, task_queue
from app.models import Carrier, ProduceItem, Load, LoadItem, Crop
from app.tasks import import_carriers_from_csv

# GET routes
# @app.route('/api/carriers', methods=['GET'])
# def get_carriers():
#     carriers = Carrier.query.all()
#     return jsonify([{
#         'id': carrier.id,
#         'name': carrier.name,
#         'email': carrier.email,
#         'phone': carrier.phone,
#         'company': carrier.company,
#         'address': carrier.address,
#         'allowed_items': carrier.allowed_items,
#         'max_load_quantity': carrier.max_load_quantity
#     } for carrier in carriers]), 200    

# testing a carrier
@app.route('/api/carriers', methods=['GET'])
def list_carriers():
    carriers = Carrier.query.all()
    results = []
    for carrier in carriers:
        results.append({
            'id': carrier.id,
            'name': carrier.name,
            'email': carrier.email,
            'phone': carrier.phone,
            'company': carrier.company
        })
    return jsonify(results), 200

@app.route('/loads', methods=['GET'])
def get_loads():
    loads = Load.query.all()
    return jsonify([{
        'id': load.id,
        'customer': load.customer,
        'carrier_id': load.carrier_id,
        'status': load.status,
        'load_items': [{
            'produce_item_id': item.produce_item_id,
            'quantity': item.quantity
        } for item in load.load_items]
    } for load in loads]), 200

@app.route('/produce_items', methods=['GET'])
def get_produce_items():
    produce_items = ProduceItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'unit': item.unit,
        'category': item.category
    } for item in produce_items]), 200  
    
# health code status
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

# old code
# from flask import request, jsonify
# from app import app, db
# from models import Carrier, Load, ProduceItem

# @app.route('/carriers', methods=['GET'])
# def get_carriers():
#     carriers = Carrier.query.all()
#     return jsonify([carrier.to_dict() for carrier in carriers])

# @app.route('/loads', methods=['GET'])
# def get_loads():
#     loads = Load.query.all()
#     return jsonify([load.to_dict() for load in loads])

# @app.route('/produce_items', methods=['GET'])
# def get_produce_items():
#     produce_items = ProduceItem.query.all()
#     return jsonify([item.to_dict() for item in produce_items])

# @app.route('/carriers', methods=['POST'])
# def add_carrier():
#     data = request.get_json()
#     new_carrier = Carrier(**data)
#     db.session.add(new_carrier)
#     db.session.commit()
#     return jsonify(new_carrier.to_dict()), 201

# @app.route('/loads', methods=['POST'])
# def add_load():
#     data = request.get_json()
#     new_load = Load(**data)
#     db.session.add(new_load)
#     db.session.commit()
#     return jsonify(new_load.to_dict()), 201

# from flask import Blueprint, request, jsonify
# from .models import db, ProduceItem, Carrier, Load
# from .tasks import process_csv
# from .utils import validate_carrier

# # Create a blueprint to group application routes
# main = Blueprint('main', __name__)

# @main.route('/carriers', methods=['GET'])
# def get_carriers():
#     carriers = Carrier.query.all()
#     return jsonify([carrier.to_dict() for carrier in carriers])

# @main.route('/carriers/import', methods=['POST'])
# def import_carriers():
#     csv_file = request.files['file']
#     if not csv_file:
#         return jsonify({'error': 'No file provided'}), 400

#     task = process_csv.queue(csv_file.read().decode('utf-8'))
#     return jsonify({'task_id': task.id}), 202

# # Outras rotas para loads, produce items, etc.
