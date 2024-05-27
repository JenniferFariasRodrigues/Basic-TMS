from . import db

class ProduceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)

class Carrier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    produce_items = db.relationship('ProduceItem', backref='carrier', lazy=True)
    is_busy = db.Column(db.Boolean, default=False)

class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    produce_items = db.relationship('ProduceItem', backref='load', lazy=True)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'))
    carrier = db.relationship('Carrier', backref='loads')
