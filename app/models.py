from . import db
from sqlalchemy.orm import validates

class ValidationError(Exception):
    pass

# Associative table, used to represent a many-to-many relationship
load_produce_item = db.Table('load_produce_item',
                             db.Column('load_id', db.Integer, db.ForeignKey('load.id'), primary_key=True),
                             db.Column('produce_item_id', db.Integer, db.ForeignKey('produce_item.id'),
                                       primary_key=True)
                             )
class ProduceItem(db.Model):
    __tablename__ = 'produce_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(32), nullable=False, default='Caixa')
    category = db.Column(db.String(32), nullable=False)
    carriers = db.relationship('Carrier', secondary='carrier_produce_item', back_populates='produce_items')
    loads = db.relationship('Load', secondary=load_produce_item, back_populates='produce_items')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'category': self.category
        }

class Carrier(db.Model):
    __tablename__ = 'carrier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    allowed_items = db.Column(db.JSON, nullable=True)
    max_load_quantity = db.Column(db.Integer, nullable=False)
    produce_items = db.relationship('ProduceItem', secondary='carrier_produce_item', back_populates='carriers')
    loads = db.relationship('Load', back_populates='carrier')

    @property
    def is_busy(self):
        return any(load.status != 'delivered' for load in self.loads)

    def can_carry_all_items(self, load):
        if 'any' in self.allowed_items:
            return are_items_compatible([item.produce_item for item in load.load_items])
        for load_item in load.load_items:
            if load_item.produce_item.name not in self.allowed_items:
                return False
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


class CarrierProduceItem(db.Model):
    __tablename__ = 'carrier_produce_item'
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), primary_key=True)


def are_items_compatible(items):
    incompatible_pairs = [
        ('maca', 'broccoli'),
        ('banana', 'lettuce'),
        ('tomate', 'cucumber'),
        ('batata', 'cebola'),
        ('morango', 'cebola'),
        ('blueberries', 'cebola'),
        ('melao', None)
    ]
    item_names = [item.name for item in items]
    for pair in incompatible_pairs:
        if pair[1] is None and pair[0] in item_names:
            if len(item_names) > 1:
                return False
        elif pair[0] in item_names and pair[1] in item_names:
            return False
    return True


class Load(db.Model):
    __tablename__ = 'load'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(64), nullable=False)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), nullable=True)
    carrier = db.relationship('Carrier', back_populates='loads')
    produce_items = db.relationship('ProduceItem', secondary=load_produce_item, back_populates='loads')
    load_items = db.relationship('LoadItem', back_populates='load', lazy=True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # customer = db.relationship('Customer', back_populates='loads')
    # status = db.Column(db.String(20), nullable=False, default='pending')

    @validates('carrier_id')
    def validate_carrier(self, key, carrier_id):
        carrier = Carrier.query.get(carrier_id)
        if not carrier:
            raise ValidationError("Carrier not found")
        if carrier.is_busy:
            raise ValidationError(f"Carrier {carrier.name} is busy!")

        if not carrier.can_carry_all_items(self):
            raise ValidationError(f"Carrier {carrier.name} Can't carry all these load items!")

        if not carrier.can_carry_quantity(self):
            unit = self.load_items[0].produce_item.unit if self.load_items else 'unity'
            total_quantity_in_load = sum(load_item.quantity for load_item in self.load_items)
            current_total_quantity = sum(
                sum(load_item.quantity for load_item in existing_load.load_items)
                for existing_load in carrier.loads
            )
            raise ValidationError(f"Carrier {carrier.name} cannot load more than "
                                  f"{carrier.max_load_quantity} {unit} load itens! Current quantity: "
                                  f"{current_total_quantity} {unit}, Attempt to add:"
                                  f" {total_quantity_in_load} {unit}.")

        if not are_items_compatible([item.produce_item for item in self.load_items]):
            raise ValidationError("Load items are not compatible!.")
        return carrier_id

    def validate_load_items(self):
        if not are_items_compatible([item.produce_item for item in self.load_items]):
            raise ValidationError("Load items are not compatible!")

    def as_dict(self):
        return {
            'id': self.id,
            'customer': self.customer,
            'carrier_id': self.carrier_id,
            'carrier': self.carrier.as_dict() if self.carrier else None,
            'load_items': [item.as_dict() for item in self.load_items]
        }


class LoadItem(db.Model):
    __tablename__ = 'load_item'
    id = db.Column(db.Integer, primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    load_id = db.Column(db.Integer, db.ForeignKey('load.id'), nullable=False)
    produce_item = db.relationship('ProduceItem')
    load = db.relationship('Load', back_populates='load_items')

    def as_dict(self):
        return {
            'id': self.id,
            'produce_item_id': self.produce_item_id,
            'quantity': self.quantity,
            'load_id': self.load_id,
            'produce_item': self.produce_item.as_dict()
        }


class Crop(db.Model):
    __tablename__ = 'crop'
    id = db.Column(db.Integer, primary_key=True)
    produce_item_id = db.Column(db.Integer, db.ForeignKey('produce_item.id'), nullable=False)
    carrier_id = db.Column(db.Integer, db.ForeignKey('carrier.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    farmer = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    produce_item = db.relationship('ProduceItem')
    carrier = db.relationship('Carrier')

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
# class Customer(db.Model):
#     __tablename__ = 'customer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     phone = db.Column(db.String(20), nullable=False)
#     loads = db.relationship('Load', back_populates='customer')
#
#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'address': self.address,
#             'email': self.email,
#             'phone': self.phone,
#             'loads': [load.as_dict() for load in self.loads]
#         }