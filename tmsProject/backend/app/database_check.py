from config import db, app
from models import Carrier, Load
# This function check all the data about database
def query_loads():
    try:
        print("Starting carrier query...")
        carriers = Carrier.query.all()
        print(f"Total loads found: {len(carriers)}")
        if not carriers:    
            print("No carries found in the database.")
        for carrier in carriers:
            print(f"Carrier ID: {carrier.id}")
            print(f"Name: {carrier.name}")
            print(f"Email: {carrier.email}")
            print(f"Phone: {carrier.phone}")
            print(f"Company: {carrier.company}")
            print(f"Address: {carrier.address}")
            print(f"Allowed Items: {carrier.allowed_items}")
            print(f"Status: {carrier.status}")
            print(f"Max Load Quantity: {carrier.max_load_quantity}")
            print('---')
            for load in carrier.loads:
                    print(f"Load ID: {load.id}")
                    print(f"Customer: {load.customer}")
                    print("Production Items:")
                    for load_item in load.load_items:
                        print(f"   - {load_item.produce_item.name}: {load_item.quantity} {load_item.produce_item.unit}")
                    print("  -----")
            print("-----")
    except Exception as e:
        print(f"Error when querying loads: {e}")

# It calls the function'
if __name__ == "__main__":
    with app.app_context():
        query_loads()