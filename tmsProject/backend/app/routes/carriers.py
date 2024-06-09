from flask import Blueprint, request, jsonify
from config import db
from models import Carrier
from tasks.import_carriers import import_carriers_from_csv

carriers_bp = Blueprint('carriers', __name__)

@carriers_bp.route('/carriers', methods=['GET'])
def list_carriers():
    carriers = Carrier.query.all()
    return jsonify([carrier.to_dict() for carrier in carriers])

@carriers_bp.route('/carriers', methods=['POST'])
def create_carrier():
    data = request.json
    carrier = Carrier(**data)
    db.session.add(carrier)
    db.session.commit()
    return jsonify(carrier.to_dict()), 201

@carriers_bp.route('/carriers/import', methods=['POST'])
def import_carriers():
    file = request.files['file']
    import_carriers_from_csv(file)
    return jsonify({'message': 'Carriers imported successfully'}), 200
