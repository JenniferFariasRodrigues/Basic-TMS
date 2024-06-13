import csv
import requests

BASE_URL = 'http://localhost:5000'

def handle_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    try:
        response_json = response.json()
        print(response_json)
        return response_json
    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format")
        return None

def insert_carriers_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            payload = {
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone'],
                'company': row['company'],
                'address': row['address'],
                'max_load_quantity': int(row['max_load_quantity']),
                'allowed_items': row['allowed_items'].strip("[]").replace("'", "").split(", ")
            }
            response = requests.post(f"{BASE_URL}/carriers", json=payload)
            handle_response(response)

if __name__ == "__main__":
    insert_carriers_from_csv('carriers.csv')
