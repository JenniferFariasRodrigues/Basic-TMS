from sqlalchemy import JSON
from . import db
from sqlalchemy.orm import validates

class ValidationError(Exception):
    pass

# Associative table, used to represent a many-to-many relationship
load_produce_item = db.Table('load_produce_item',
    db.Column('load_id', db.Integer, db.ForeignKey('load.id'), primary_key=True),
    db.Column('produce_item_id', db.Integer, db.ForeignKey('produce_item.id'),
    primary_key=True))                          
# This represents a agricultural product/item and defines a many-to-many relationship between ProduceItem and Carrier
class ProduceItem(db.Model):
    # It defines the columns of the produce_item table
    __tablename__ = 'produce_item' # The table name ensures that the tables are produced with these names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(32), nullable=False, default='Box')
    category = db.Column(db.String(32), nullable=False)
    carriers = db.relationship('Carrier', secondary='carrier_produce_item', back_populates='produce_items')# This defines a many-to-many relationship between ProduceItem and Carrier through the carrier_produce_item associative table.
    loads = db.relationship('Load', secondary=load_produce_item, back_populates='produce_items')
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'category': self.category
        }
    
# This represent a columns table Carrier and the many-to-many relationship with ProduceItem code 
# through the carrier_produce_item table.
class Carrier(db.Model):
    # It defines the columns of the carrier 
    __tablename__ = 'carrier'# The table name ensures that the tables are produced with these names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    allowed_items = db.Column(JSON, nullable=True)  # This indicates which products are compatible with the charger
    max_load_quantity = db.Column(db.Integer, nullable=False)
    produce_items = db.relationship('ProduceItem', secondary='carrier_produce_item', back_populates='carriers') # Relationship beteween ProduceItem and carrier_produce_item
    loads = db.relationship('Load', back_populates='carrier')# Checks whether the Carrier is busy. A carrier is busy if it has any load with a status other than delivered.A Carrier can have many Loads. Each Load belongs to a single Carrier.
    
    @property
    def is_busy(self):
        return any(load.status != 'delivered' for load in self.loads)       
    def can_carry_all_items(self, load):
        # Checks if the carrier can load any item
        if 'any' in self.allowed_items:
            return are_items_compatible([item.produce_item for item in load.load_items])

        # Checks if all items in the load are allowed
        for load_item in load.load_items:
            if load_item.produce_item.name not in self.allowed_items:
                return False

        # Check item compatibility
        return are_items_compatible([item.produce_item for item in load.load_items])

    def can_carry_quantity(self, load):
        total_quantity = sum(
            sum(load_item.quantity for load_item in existing_load.load_items)
            for existing_load in self.loads
        )
        total_quantity += sum(load_item.quantity for load_item in load.load_items)
        return total_quantity <= self.max_load_quantity
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'address': self.address,
            'allowed_items': self.allowed_items,
            'max_load_quantity': self.max_load_quantity
        }


# This represents a many-to-many relationship between Carrier and ProduceItem.
class CarrierProduceItem(db.Model):
    __tablename__ = 'carrier_produce_item'
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
        ('strawberry', 'onion'),
        ('blueberries', 'onion'),
        ('melon', None)  
    ]
    # This extracts the production item names from the given item list.
    item_names = [item.name for item in items]     
    for pair in incompatible_pairs:#This check the list of items for incompatible pairs. 
        if pair[1] is None and pair[0] in item_names:# If there is,it returns False, indicating that the items are not compatible.
            if len(item_names) > 1:
                return False
        elif pair[0] in item_names and pair[1] in item_names:
            return False
    return True

class Load(db.Model):
    # It defines the columns of the load table
    __tablename__ = 'load'
    id = db.Column(db.Integer, primary_key=True)   
    customer = db.Column(db.String(64), nullable=False)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), nullable=True)
    carrier = db.relationship('Carrier', back_populates='loads')
    produce_items = db.relationship('ProduceItem', secondary=load_produce_item, back_populates='loads')
    load_items = db.relationship('LoadItem', back_populates='load', lazy=True)# This defines a one-to-many relationship between Load and LoadItem.
    # status = db.Column(db.String(50), default='pending')
    

    #Validation: this validates that the carrier can be assigned to the load.
    # called when a Carrier is assigned to a Load. It checks whether the carrier is busy 
    # and whether the items in the load are compatible with each other. If any of these conditions fail,
    # an exception is thrown.
    @validates('carrier_id')
    def validate_carrier(self, key, carrier_id):
        carrier = Carrier.query.get(carrier_id)
        if not carrier:
            raise ValidationError("Carrier not found.")
        if carrier.is_busy:
            raise ValidationError(f"The carrier {carrier.name} is busy.")
        if not carrier.can_carry_all_items(self):
            raise ValidationError(f"The carrier {carrier.name} cannot carry all of these load items!")
        if not carrier.can_carry_quantity(self):
            unit = self.load_items[0].produce_item.unit if self.load_items else 'unit'
            total_quantity_in_load = sum(load_item.quantity for load_item in self.load_items)
            current_total_quantity = sum(sum(load_item.quantity for load_item in existing_load.load_items)
                for existing_load in carrier.loads
            )
            raise ValidationError(f"The carrier {carrier.name} cannot load more than "
                f"{carrier.max_load_quantity} {unit} of load items! Current quantity: "
                f"{current_total_quantity} {unit}, Attempt to add: "
                f"{total_quantity_in_load} {unit}.")
        if not are_items_compatible([item.produce_item for item in self.load_items]):
            raise ValidationError("Load items are not compatible")
        return carrier_id


    # Validation: this validates that the items in the load are compatible with each other.
    # called when load items are added to a Load. It checks whether the items in the load are
    # compatible with each other. If they are not compatible, an exception is thrown.
    def validate_load_items(self):
        if not are_items_compatible([item.produce_item for item in self.load_items]):
            raise ValidationError("Load items are not compatible")
        
    def as_dict(self):
        return {
            'id': self.id,
            'customer': self.customer,
            'carrier_id': self.carrier_id,
            'carrier': self.carrier.as_dict() if self.carrier else None,
            'load_items': [item.as_dict() for item in self.load_items]
        }
        

class LoadItem(db.Model):
    # It define the columns of the loadItem table
    __tablename__ = 'load_item'    
    id = db.Column(db.Integer, primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    load_id = db.Column(db.Integer, db.ForeignKey('load.id'), nullable=False)# ForeignKeys: table references ProduceItem and Load.
    produce_item = db.relationship('ProduceItem')# This defines a many-to-one relationship between LoadItem and ProduceItem.
    load = db.relationship('Load', back_populates='load_items')#This defines a many-to-one relationship between LoadItem and Load.
    
    def as_dict(self):
        return {
            'id': self.id,
            'produce_item_id': self.produce_item_id,
            'quantity': self.quantity,
            'load_id': self.load_id,
            'produce_item': self.produce_item.as_dict()
        }


class Crop(db.Model):
    # It defines the columns of the crop table.
    __tablename__ = 'crop'
    id = db.Column(db.Integer, primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), nullable=False)    
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), nullable=False)# ForeignKey: this table references ProduceItem and Carrier.
    quantity = db.Column(db.Integer, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False) # Stores Harvest Date: Track the freshness and expiration of harvested items.Many agricultural products have a limited shelf life and the harvest date 
    farmer = db.Column(db.String(100), nullable=False) 
    location = db.Column(db.String(100), nullable=False)
    produce_item = db.relationship('ProduceItem')# This defines the many-to-one relationship between Crop and ProduceItem.
    carrier = db.relationship('Carrier') # This defines the many-to-one relationship between Crop and Carrier. 
    
    def as_dict(self):
        return {
            'id': self.id,
            'produce_item_id': self.produce_item_id,
            'carrier_id': self.carrier_id,
            'quantity': self.quantity,
            'harvest_date': self.harvest_date,
            'farmer': self.farmer,
            'location': self.location,
            'produce_item': self.produce_item.as_dict(),
            'carrier': self.carrier.as_dict()
        }
