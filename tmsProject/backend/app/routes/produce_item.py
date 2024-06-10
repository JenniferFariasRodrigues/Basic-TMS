from flask import Blueprint, request, jsonify
from config import db
from models import ProduceItem

produce_items_bp = Blueprint('produce_items', __name__)

@produce_items_bp.route('/produce_items', methods=['GET'])
def list_produce_items():
    produce_items = ProduceItem.query.all()
    return jsonify([item.to_dict() for item in produce_items])

@produce_items_bp.route('/produce_items', methods=['POST'])
def create_produce_item():
    data = request.json
    produce_item = ProduceItem(**data)
    db.session.add(produce_item)
    db.session.commit()
    return jsonify(produce_item.to_dict()), 201
