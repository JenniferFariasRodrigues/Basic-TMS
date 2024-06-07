from . import db
from sqlalchemy.orm import validates # type: ignore
from sqlalchemy.exc import ValidationError # type: ignore

# This represents a agricultural product/item.
class ProduceItem(db.Model):
    # It defines the columns of the produce_item table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    #This defines a many-to-many relationship between ProduceItem and Carrier
    # through the carrier_produce_item associative table.
    carriers = db.relationship('Carrier', secondary='carrier_produce_item', back_populates='produce_items')

    
# This is a many-to-many relationship with ProduceItem code through the carrier_produce_item table
class Carrier(db.Model):
    # It defines the columns of the carrier table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    #Relationship beteween ProduceItem and carrier_produce_item
    produce_items = db.relationship('ProduceItem', secondary='carrier_produce_item', back_populates='carriers')
    #This defines a one-to-many relationship between Carrier and Load.
    loads = db.relationship('Load', back_populates='carrier')    
    # Checks whether the Carrier is busy. A carrier is busy if it has 
    # any cargo with a status other than delivered.
    @property
    def is_busy(self):
        return any(load.status != 'delivered' for load in self.loads)

# This represents a many-to-many relationship between Carrier and ProduceItem.
class CarrierProduceItem(db.Model):
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), primary_key=True)

# Helper function to check incompatibilities between itemsdef are_items_compatible(items):
# Check that the items in a load are compatible with each other. If there are incompatibilities,
# the function returns False.E.g., Melon cannot be transported with any other .
def are_items_compatible(items):
    # List of incompatible pairs.
    incompatible_pairs = [
        ('apple', 'broccoli'),
        ('banana', 'lettuce'),
        ('tomato', 'cucumber'),
        ('potato', 'onion'),
        ('melon', None)  
    ]
    # This extracts the production item names from the given item list.
    item_names = [item.produce_item.name for item in items]
    #This check the list of items for incompatible pairs. If there is, 
    # it returns False, indicating that the items are not compatible.
    for pair in incompatible_pairs:
        if pair[1] is None and pair[0] in item_names:
            if len(item_names) > 1:
                return False
        elif pair[0] in item_names and pair[1] in item_names:
            return False

    return True
class Load(db.Model):
    # It defines the columns of the load table
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(50), default='pending')
    produce_items = db.relationship('ProduceItem', backref='load', lazy=True)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), nullable=True)
    # This defines a many-to-one relationship between Load and Carrier.
    carrier = db.relationship('Carrier', back_populates='loads')
    # This defines a one-to-many relationship between Load and LoadItem.
    load_items = db.relationship('LoadItem', back_populates='load', lazy=True)

    #Validation: this validates that the carrier can be assigned to the load.
    # called when a Carrier is assigned to a Load. It checks whether the carrier is busy 
    # and whether the items in the load are compatible with each other. If any of these conditions fail,
    # an exception is thrown.
    @validates('carrier_id')
    def validate_carrier(self, key, carrier_id):
        carrier = Carrier.query.get(carrier_id)
        if carrier.is_busy:
            raise ValidationError("Carrier is busy")
        if not are_items_compatible(self.load_items):
            raise ValidationError("Load items are not compatible")
        return carrier_id

    # Validation: this validates that the items in the load are compatible with each other.
    # called when load items are added to a Load. It checks whether the items in the load are
    # compatible with each other. If they are not compatible, an exception is thrown.
    @validates('load_items')
    def validate_load_items(self, key, load_items):
        if not are_items_compatible(load_items):
            raise ValidationError("Load items are not compatible")
        return load_items
