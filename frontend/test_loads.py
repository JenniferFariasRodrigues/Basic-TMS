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

class TestLoads(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clean_database()

    @classmethod
    def tearDownClass(cls):
        cls.clean_database()

    @classmethod
    def clean_database(cls):
        url = f"{BASE_URL}/loads"
        response = requests.get(url)
        items = handle_response(response)
        if items:
            for item in items:
                delete_url = f"{url}/{item['id']}"
                delete_response = requests.delete(delete_url)
                handle_response(delete_response)

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
