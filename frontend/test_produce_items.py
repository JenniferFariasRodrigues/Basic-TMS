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

class TestProduceItems(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clean_database()

    @classmethod
    def tearDownClass(cls):
        cls.clean_database()

    @classmethod
    def clean_database(cls):
        url = f"{BASE_URL}/produce_items"
        response = requests.get(url)
        items = handle_response(response)
        if items:
            for item in items:
                delete_url = f"{url}/{item['id']}"
                delete_response = requests.delete(delete_url)
                handle_response(delete_response)

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

if __name__ == "__main__":
    unittest.main()
