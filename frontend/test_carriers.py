import unittest
import requests
import json

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

class TestCarriers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clean_database()

    @classmethod
    def tearDownClass(cls):
        cls.clean_database()

    @classmethod
    def clean_database(cls):
        url = f"{BASE_URL}/carriers"
        response = requests.get(url)
        items = handle_response(response)
        if items:
            for item in items:
                delete_url = f"{url}/{item['id']}"
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

if __name__ == "__main__":
    unittest.main()
