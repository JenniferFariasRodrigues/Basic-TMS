from config import db, app
from models import Load
# This function check all the data about database
def query_loads():
    try:
        loads = Load.query.all()
        for load in loads:
            print(f"Load ID: {load.id}")
            print(f"Cliente: {load.customer}")
            print(f"Carrier: {load.carrier.name if load.carrier else 'None'}")
            print("Production Items:")
            for load_item in load.load_items:
                print(f" - {load_item.produce_item.name}: {load_item.quantity} {load_item.produce_item.unit}")
            print("-----")
    except Exception as e:
        print(f"Error when querying loads: {e}")

# It calls the function'
if __name__ == "__main__":
    with app.app_context():
        query_loads()