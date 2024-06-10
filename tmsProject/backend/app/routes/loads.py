from flask import Blueprint, request, jsonify
from config import db
from models import Load

loads_bp = Blueprint('loads', __name__)

@loads_bp.route('/loads', methods=['GET'])
def list_loads():
    loads = Load.query.all()
    return jsonify([load.to_dict() for load in loads])

@loads_bp.route('/loads', methods=['POST'])
def create_load():
    data = request.json
    load = Load(**data)
    db.session.add(load)
    db.session.commit()
    return jsonify(load.to_dict()), 201
