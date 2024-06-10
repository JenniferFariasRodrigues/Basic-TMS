from flask import request, jsonify
from app import app, db
from models import Carrier, Load, ProduceItem

@app.route('/carriers', methods=['GET'])
def get_carriers():
    carriers = Carrier.query.all()
    return jsonify([carrier.to_dict() for carrier in carriers])

@app.route('/loads', methods=['GET'])
def get_loads():
    loads = Load.query.all()
    return jsonify([load.to_dict() for load in loads])

@app.route('/produce_items', methods=['GET'])
def get_produce_items():
    produce_items = ProduceItem.query.all()
    return jsonify([item.to_dict() for item in produce_items])

@app.route('/carriers', methods=['POST'])
def add_carrier():
    data = request.get_json()
    new_carrier = Carrier(**data)
    db.session.add(new_carrier)
    db.session.commit()
    return jsonify(new_carrier.to_dict()), 201

@app.route('/loads', methods=['POST'])
def add_load():
    data = request.get_json()
    new_load = Load(**data)
    db.session.add(new_load)
    db.session.commit()
    return jsonify(new_load.to_dict()), 201

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
