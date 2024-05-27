from flask import Blueprint, request, jsonify
from .models import db, ProduceItem, Carrier, Load
from .tasks import process_csv
from .utils import validate_carrier

main = Blueprint('main', __name__)

@main.route('/carriers', methods=['GET'])
def get_carriers():
    carriers = Carrier.query.all()
    return jsonify([carrier.to_dict() for carrier in carriers])

@main.route('/carriers/import', methods=['POST'])
def import_carriers():
    csv_file = request.files['file']
    if not csv_file:
        return jsonify({'error': 'No file provided'}), 400

    task = process_csv.queue(csv_file.read().decode('utf-8'))
    return jsonify({'task_id': task.id}), 202

# Outras rotas para loads, produce items, etc.
