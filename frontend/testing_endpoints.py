import unittest
import requests
import json
from app import create_app, db  # Certifique-se de que o módulo app está no PYTHONPATH

BASE_URL = 'http://localhost:5000'
def handle_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    try:
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
        return response_json
    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format")
        return None

class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.clean_database()

    def tearDown(self):
        self.clean_database()

    def clean_database(self):
        endpoints = [
            f"{BASE_URL}/carriers",
            f"{BASE_URL}/produce_items",
            f"{BASE_URL}/loads"
        ]
        for endpoint in endpoints:
            response = requests.get(endpoint)
            items = handle_response(response)
            if items:
                for item in items:
                    delete_url = f"{endpoint}/{item['id']}"
                    delete_response = requests.delete(delete_url)
                    handle_response(delete_response)

    def test_create_carrier(self):
        url = f"{BASE_URL}/carriers"
        payload = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890',
            'company': 'JD Transport',
            'address': '123 Main St',
            'max_load_quantity': 50,
            'allowed_items': ['banana', 'tomato']
        }
        response = requests.post(url, json=payload)
        print("Create Carrier:")
        handle_response(response)

    def test_get_carriers(self):
        url = f"{BASE_URL}/carriers"
        response = requests.get(url)
        print("Get Carriers:")
        handle_response(response)

    def test_get_carrier(self):
        self.test_create_carrier()
        carrier_id = 1  # Assumindo que este é o ID do carrier criado
        url = f"{BASE_URL}/carriers/{carrier_id}"
        response = requests.get(url)
        print("Get Carrier:")
        handle_response(response)

    def test_update_carrier(self):
        self.test_create_carrier()
        carrier_id = 1  # Assumindo que este é o ID do carrier criado
        url = f"{BASE_URL}/carriers/{carrier_id}"
        payload = {
            'name': 'John Updated',
            'email': 'johndoe@example.com',
            'phone': '0987654321',
            'company': 'JD Updated Transport',
            'address': '456 Elm St',
            'max_load_quantity': 100,
            'allowed_items': ['strawberry', 'blueberry']
        }
        response = requests.put(url, json=payload)
        print("Update Carrier:")
        handle_response(response)

    def test_delete_carrier(self):
        self.test_create_carrier()
        carrier_id = 1  # Assumindo que este é o ID do carrier criado
        url = f"{BASE_URL}/carriers/{carrier_id}"
        response = requests.delete(url)
        print("Delete Carrier:")
        handle_response(response)

    def test_create_produce_item(self):
        url = f"{BASE_URL}/produce_items"
        payload = {
            'name': 'Banana',
            'unit': 'Caixa',
            'category': 'fruit'
        }
        response = requests.post(url, json=payload)
        print("Create Produce Item:")
        handle_response(response)

    def test_get_produce_items(self):
        url = f"{BASE_URL}/produce_items"
        response = requests.get(url)
        print("Get Produce Items:")
        handle_response(response)

    def test_get_produce_item(self):
        self.test_create_produce_item()
        produce_item_id = 1  # Assumindo que este é o ID do produce item criado
        url = f"{BASE_URL}/produce_items/{produce_item_id}"
        response = requests.get(url)
        print("Get Produce Item:")
        handle_response(response)

    def test_update_produce_item(self):
        self.test_create_produce_item()
        produce_item_id = 1  # Assumindo que este é o ID do produce item criado
        url = f"{BASE_URL}/produce_items/{produce_item_id}"
        payload = {
            'name': 'Banana Updated',
            'unit': 'Box',
            'category': 'fruit'
        }
        response = requests.put(url, json=payload)
        print("Update Produce Item:")
        handle_response(response)

    def test_delete_produce_item(self):
        self.test_create_produce_item()
        produce_item_id = 1  # Assumindo que este é o ID do produce item criado
        url = f"{BASE_URL}/produce_items/{produce_item_id}"
        response = requests.delete(url)
        print("Delete Produce Item:")
        handle_response(response)

    def test_create_load(self):
        url = f"{BASE_URL}/loads"
        payload = {
            'customer': 'Customer A'
        }
        response = requests.post(url, json=payload)
        print("Create Load:")
        handle_response(response)

    def test_get_loads(self):
        url = f"{BASE_URL}/loads"
        response = requests.get(url)
        print("Get Loads:")
        handle_response(response)

    def test_get_load(self):
        self.test_create_load()
        load_id = 1  # Assumindo que este é o ID do load criado
        url = f"{BASE_URL}/loads/{load_id}"
        response = requests.get(url)
        print("Get Load:")
        handle_response(response)

    def test_update_load(self):
        self.test_create_load()
        load_id = 1  # Assumindo que este é o ID do load criado
        url = f"{BASE_URL}/loads/{load_id}"
        payload = {
            'customer': 'Customer B',
            'carrier_id': 1  # Certifique-se de que um carrier com este ID existe
        }
        response = requests.put(url, json=payload)
        print("Update Load:")
        handle_response(response)

    def test_delete_load(self):
        self.test_create_load()
        load_id = 1  # Assumindo que este é o ID do load criado
        url = f"{BASE_URL}/loads/{load_id}"
        response = requests.delete(url)
        print("Delete Load:")
        handle_response(response)

if __name__ == "__main__":
    unittest.main()
