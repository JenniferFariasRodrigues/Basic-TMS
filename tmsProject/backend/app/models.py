from . import db

#agricultural product/item
class ProduceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    
# many-to-many relationship with ProduceItem code through the carrier_produce_item table
class Carrier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    #relationship beteween ProduceItem and carrier_produce_item
    produce_items = db.relationship('ProduceItem', secondary='carrier_produce_item', back_populates='carriers')

# many-to-many relationship between Carrier and ProduceItem
class CarrierProduceItem(db.Model):
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), primary_key=True)

class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    produce_items = db.relationship('ProduceItem', backref='load', lazy=True)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'))
    carrier = db.relationship('Carrier', backref='loads')
