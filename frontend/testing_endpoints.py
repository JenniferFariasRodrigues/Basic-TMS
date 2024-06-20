import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Carrier, ProduceItem, Load, Customer

class EndpointTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a Flask test client and initialize the database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:tmsdbtest:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_sample_data(self):
        """Create sample data for testing."""
        customer = Customer(name="Customer A")
        carrier = Carrier(
            name='Carrier A',
            email='carrierA@example.com',
            phone='1234567890',
            company='Company A',
            address='Address A',
            max_load_quantity=10,
            allowed_items=['Apple', 'Banana']
        )
        produce_item = ProduceItem(
            name='Apple',
            unit='kg',
            category='Fruit'
        )
        db.session.add(customer)
        db.session.add(carrier)
        db.session.add(produce_item)
        db.session.commit()
        return customer, carrier, produce_item

    # Test Carriers
    def test_create_carrier(self):
        carrier_data = {
            'name': 'Carrier A',
            'email': 'carrierA@example.com',
            'phone': '1234567890',
            'company': 'Company A',
            'address': 'Address A',
            'max_load_quantity': 10,
            'allowed_items': ['Apple', 'Banana']
        }
        response = self.client.post('/carriers', data=json.dumps(carrier_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_carriers(self):
        self.test_create_carrier()
        response = self.client.get('/carriers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_carrier(self):
        self.test_create_carrier()
        updated_data = {
            'name': 'Carrier A Updated',
            'email': 'carrierA@example.com',
            'phone': '1234567890',
            'company': 'Company A',
            'address': 'Address A',
            'max_load_quantity': 20,
            'allowed_items': ['Apple', 'Banana']
        }
        response = self.client.put('/carriers/1', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_carrier(self):
        self.test_create_carrier()
        response = self.client.delete('/carriers/1')
        self.assertEqual(response.status_code, 200)

    # Test Produce Items
    def test_create_produce_item(self):
        produce_item_data = {
            'name': 'Apple',
            'unit': 'kg',
            'category': 'Fruit'
        }
        response = self.client.post('/produce_items', data=json.dumps(produce_item_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_produce_items(self):
        self.test_create_produce_item()
        response = self.client.get('/produce_items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_produce_item(self):
        self.test_create_produce_item()
        updated_data = {
            'name': 'Apple Updated',
            'unit': 'kg',
            'category': 'Fruit'
        }
        response = self.client.put('/produce_items/1', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_produce_item(self):
        self.test_create_produce_item()
        response = self.client.delete('/produce_items/1')
        self.assertEqual(response.status_code, 200)

    # Test Loads
    def test_create_load(self):
        customer, carrier, produce_item = self.create_sample_data()
        load_data = {
            'customer_id': customer.id,
            'status': 'pending',
            'carrier_id': carrier.id
        }
        response = self.client.post('/loads', data=json.dumps(load_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_loads(self):
        self.test_create_load()
        response = self.client.get('/loads')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_load(self):
        self.test_create_load()
        updated_data = {
            'customer_id': 1,
            'status': 'delivered',
            'carrier_id': 1
        }
        response = self.client.put('/loads/1', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_load(self):
        self.test_create_load()
        response = self.client.delete('/loads/1')
        self.assertEqual(response.status_code, 200)

    # Test Customers
    def test_create_customer(self):
        customer_data = {'name': 'Customer A'}
        response = self.client.post('/customers', data=json.dumps(customer_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_customers(self):
        self.test_create_customer()
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_customer(self):
        self.test_create_customer()
        updated_data = {'name': 'Customer A Updated'}
        response = self.client.put('/customers/1', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        self.test_create_customer()
        response = self.client.delete('/customers/1')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
