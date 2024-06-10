import csv
from config import db
from models import Carrier

def import_carriers_from_csv(file):
    reader = csv.DictReader(file)
    for row in reader:
        carrier = Carrier(
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
            company=row['company'],
            address=row['address'],
            allowed_items=row['allowed_items'].split(','),
            max_load_quantity=row['max_load_quantity']
        )
        db.session.add(carrier)
    db.session.commit()
