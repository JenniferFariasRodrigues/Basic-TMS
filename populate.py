import csv
import requests

BASE_URL = "http://localhost:5000"

def create_customer(name):
    url = f"{BASE_URL}/customers"
    payload = {"name": name}
    response = requests.post(url, json=payload)
    return response.json()

def create_carrier(name, email, phone, company, address, max_load_quantity, allowed_items):
    url = f"{BASE_URL}/carriers"
    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "address": address,
        "max_load_quantity": max_load_quantity,
        "allowed_items": allowed_items.split(',')
    }
    response = requests.post(url, json=payload)
    return response.json()

def create_produce_item(name, unit, category):
    url = f"{BASE_URL}/produce_items"
    payload = {
        "name": name,
        "unit": unit,
        "category": category
    }
    response = requests.post(url, json=payload)
    return response.json()

def create_load(customer_id, status, carrier_id):
    url = f"{BASE_URL}/loads"
    payload = {
        "customer_id": customer_id,
        "status": status,
        "carrier_id": carrier_id
    }
    response = requests.post(url, json=payload)
    return response.json()

def create_load_item(load_id, produce_item_id, quantity):
    url = f"{BASE_URL}/load_items"
    payload = {
        "load_id": load_id,
        "produce_item_id": produce_item_id,
        "quantity": quantity
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['type'] == 'customer':
                create_customer(row['name'])
            elif row['type'] == 'carrier':
                create_carrier(row['name'], row['email'], row['phone'], row['company'], row['address'], row['max_load_quantity'], row['allowed_items'])
            elif row['type'] == 'produce_item':
                create_produce_item(row['name'], row['unit'], row['category'])
            elif row['type'] == 'load':
                create_load(row['customer_id'], row['status'], row['carrier_id'])
            elif row['type'] == 'load_item':
                create_load_item(row['load_id'], row['produce_item_id'], row['quantity'])

if __name__ == "__main__":
    main()
