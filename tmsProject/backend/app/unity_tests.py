import unittest
# from config import db, app
from app import db, app

from models import ProduceItem, Carrier, Load, LoadItem, ValidationError


# It was used to perform unit tests, the unittest framework
class TestModels(unittest.TestCase):

    # This method configures a database and defines the database settings
    # system that are shared by all tests
    @classmethod # Class method
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # This method is used to clean up resources that were configured in setUpClass.
    # Just like tearDownClass, it only works once for each class call
    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # This method creates the database table and initializes the data needed for the test each time a test is run
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all() # Ensure tables are created before each test

        # Adding production items
        self.strawberry = ProduceItem(name='strawberry', unit='Box', category='fruit')
        self.blueberries = ProduceItem(name='blueberries', unit='Box', category='fruit')
        self.onion = ProduceItem(name='onion', unit='Box', category='vegetable')
        self.banana = ProduceItem(name='banana', unit='Box', category='fruit')
        self.tomato = ProduceItem(name='tomato', unit='Box', category='fruit')

        db.session.add(self.strawberry)
        db.session.add(self.blueberries)
        db.session.add(self.onion)
        db.session.add(self.banana)
        db.session.add(self.tomato)
        db.session.commit()

    # Adding carriers
        self.john = Carrier(
            name='John',
            email='john@transports.com',
            phone='123412431489',
            company='John Transportes LTDA.',
            address='Avocado street, Happy Ranch',
            allowed_items=['banana', 'tomato', 'onion'],
            max_load_quantity=10
        )
        self.mary = Carrier(
            name='Mary',
            email='mary@transports.com',
            phone='3252435146',
            company='Marys LTDA.',
            address='Avocado Street, Happy ranch',
            allowed_items=['strawberry', 'blueberries', 'blackberries'],
            max_load_quantity=20
        )
        self.steve = Carrier(
            name='Steve',
            email='steve@transports.com',
            phone='9876543210',
            company='Steve Transports LTDA.',
            address='Orange Street, Happy ranch',
            allowed_items=['any'],
            max_load_quantity=20
        )

        db.session.add(self.john)
        db.session.add(self.mary)
        db.session.add(self.steve)
        db.session.commit()

    # This method is used to remove the session from the database and delete
    # all tables after each individual test,
    # ensuring that each test starts with a clean database.
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # This test is based on the functionality of incompatible items
    # mentioned in the guidelines file. Try to check if onion and strawberry,
    # given as an example in the guidance are actually incompatible.
    def test_incompatible_items(self):
        load = Load(customer='Customer A')
        item_load1 = LoadItem(produce_item=self.strawberry, quantity=10, load=load)
        item_load2 = LoadItem(produce_item=self.onion, quantity=10, load=load)

        db.session.add(load)
        db.session.add(item_load1)
        db.session.add(item_load2)

        with self.assertRaises(ValidationError):
            load.validate_load_items()

    # This method tests the capacity validation of a carrier
    # the carrier cannot carry more items than was defined when creating the carrier
    def test_carrier_capacity(self):
        load = Load(customer='Customer B')
        item_load1 = LoadItem(produce_item=self.strawberry, quantity=10, load=load)
        item_load2 = LoadItem(produce_item=self.blueberries, quantity=10, load=load)

        db.session.add(load)
        db.session.add(item_load1)
        db.session.add(item_load2)
        db.session.commit()

        mary = Carrier.query.filter_by(name='Mary').first()
        john = Carrier.query.filter_by(name='John').first()

        self.assertTrue(mary.can_carry_quantity(load))
        self.assertFalse(john.can_carry_quantity(load))

    # This method tests whether the cargo items to be assigned to the carrier
    # are compatible with what the transporter carries. Example: The transporter can only carry strawberries and bananas
    # So, the load can only have mora and banana, if not, 
    def test_compatibilidade_e_disponibilidade_transportadora(self):
        # Check carrier disponibility and compatibility
        load1 = Load(customer='Cliente C')
        item_load1 = LoadItem(produce_item=self.strawberry, quantity=5, load=load1)
        item_load2 = LoadItem(produce_item=self.blueberries, quantity=5, load=load1)

        db.session.add(load1)
        db.session.add(item_load1)
        db.session.add(item_load2)
        db.session.commit()

        mary = Carrier.query.filter_by(name='Mary').first()
        john = Carrier.query.filter_by(name='John').first()

        self.assertTrue(mary.can_carry_all_items(load1))
        self.assertFalse(john.can_carry_all_items(load1))  # John não deve passar na compatibilidade
        self.assertFalse(mary.is_busy)
        load1.carrier = mary
        db.session.commit()
        mary.status = 'with load'
        db.session.commit()
        self.assertTrue(mary.is_busy)
        
    # The transporters Mary, Steve and John are used, with all the validations mentioned in the scenario.
    def test_complet_cenario(self):
        # Complete test scenario
        # Load 1: strawberries and blueberries
        load1 = Load(customer='Happy ranch')
        item_load1 = LoadItem(produce_item=self.strawberry, quantity=5, load=load1)
        item_load2 = LoadItem(produce_item=self.blueberries, quantity=5, load=load1)

        db.session.add(load1)
        db.session.add(item_load1)
        db.session.add(item_load2)
        db.session.commit()

        mary = Carrier.query.filter_by(name='Mary').first()
        steve = Carrier.query.filter_by(name='Steve').first()
        john = Carrier.query.filter_by(name='John').first()

        # Check carrier compatibility and capacity
        self.assertTrue(mary.can_carry_all_items(load1))
        self.assertTrue(steve.can_carry_all_items(load1))
        self.assertFalse(john.can_carry_all_items(load1)) # John must not pass compatibility

        # Check transport capacity
        self.assertTrue(mary.can_carry_quantity(load1))
        self.assertTrue(steve.can_carry_quantity(load1))
        self.assertTrue(john.can_carry_quantity(load1))

        # Assign carrier to load
        load1.carrier = mary
        db.session.commit()
        mary.status = 'with load'
        db.session.commit()
        self.assertTrue(mary.is_busy)

        # Load 2: Onions
        load2 = Load(customer='Happy ranch')
        item_load3 = LoadItem(produce_item=self.onion, quantity=10, load=load2)

        db.session.add(load2)
        db.session.add(item_load3)
        db.session.commit()

        # Check carrier compatibility and capacity
        self.assertTrue(steve.can_carry_all_items(load2))
        self.assertFalse(mary.can_carry_all_items(load2))
        self.assertTrue(john.can_carry_all_items(load2))

        # Check transport capacity
        self.assertTrue(steve.can_carry_quantity(load2))
        self.assertTrue(mary.can_carry_quantity(load2))
        self.assertTrue(john.can_carry_quantity(load2))

        # Assign carrier to load
        load2.carrier = steve
        db.session.commit()
        steve.status = 'with load'
        db.session.commit()
        self.assertTrue(steve.is_busy)
    
    def test_check_status(self):
        # Load created and input on a carrier
        load_created = Load(customer='Cliente D')
        item_load_created= LoadItem(produce_item=self.strawberry, quantity=5, load=load_created)
        
        db.session.add(load_created)
        db.session.add(item_load_created)
        db.session.commit()

        load_created.carrier = self.mary
        db.session.commit()

        # Check if carrier is busy
        self.assertTrue(self.mary.is_busy)

        load_created.status = 'delivered'
        db.session.commit()

        # check if carrier is free again
        self.assertFalse(self.mary.is_busy)


if __name__ == '__main__':
    with app.app_context():
        unittest.main() 