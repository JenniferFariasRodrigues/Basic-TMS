from config import db, app
from models import ProduceItem, Carrier, Load, LoadItem, Crop, ValidationError
from transactional import transactional_session
from datetime import date

# Used to manage transactions
@transactional_session
def insert_data():
    # Insert production items
    banana = ProduceItem(name='banana', unit='Box', category='fruit')
    tomato = ProduceItem(name='tomato', unit='Box', category='fruit')
    onion = ProduceItem(name='onion', unit='Box', category='fruit')
    melon = ProduceItem(name='melon', unit='Box', category='fruit')
    strawberry = ProduceItem(name='strawberry', unit='Box', category='fruit')
    blueberries = ProduceItem(name='blueberries', unit='Box', category='fruit')
    blackberries = ProduceItem(name='blackberries', unit='Box', category='fruit')

    db.session.add(banana)
    db.session.add(tomato)
    db.session.add(onion)
    db.session.add(melon)
    db.session.add(strawberry)
    db.session.add(blueberries)
    db.session.add(blackberries)

    # Insert carrier
    carrier1 = Carrier(
        name='John',
        email='john@transports.com',
        phone='+5548988991122',
        company='John Transportes LTDA.',
        address='Flowers Street, Happy Ranch',
        allowed_items=['banana', 'tomato', 'onion'],  # Adding the list of allowed items
        max_load_quantity=200  # Setting the maximum quantity of items
    )
    carrier2 = Carrier(
        name='Mary',
        email='mary@transports.com',
        phone='+55533252435146',
        company='Mary Transportes LTDA.',
        address='Tree Street., North Ranch',
        allowed_items=['strawberry', 'blueberries', 'amoras'],  # Adding the list of allowed items
        max_load_quantity=100  # Setting the maximum quantity of items
    )

    # carrier3 = Carrier(
    #     name='Steve',
    #     email='steve@transports.com',
    #     phone='123412431489',
    #     company='Steve Transportes LTDA.',
    #     address='Rua do abacate, Rancho feliz',
    #     allowed_items=[],  # Adicionando a lista de itens permitidos
    #     max_load_quantity=250  # Definindo a quantidade máxima de itens
    # )

    db.session.add(carrier1)
    db.session.add(carrier2)
    # db.session.add(carrier3)

    # Carrier Insert
    load1 = Load(customer='Customer A')
    load2 = Load(customer='Customer B')
    # load3 = Load(customer='Customer C')

    db.session.add(load1)
    db.session.add(load2)
    # db.session.add(load3)

    # Insert items into the load.
    load_item1 = LoadItem(produce_item=banana, quantity=100, load=load1)
    load_item2 = LoadItem(produce_item=tomato, quantity=100, load=load1)
    load_item3 = LoadItem(produce_item=strawberry, quantity=50, load=load2)
    load_item4 = LoadItem(produce_item=blueberries, quantity=50, load=load2)
    # load_item5 = LoadItem(produce_item=banana, quantity=150, load=load3)
    # load_item6 = LoadItem(produce_item=melao, quantity=150, load=load3)

    db.session.add(load_item1)
    db.session.add(load_item2)
    db.session.add(load_item3)
    db.session.add(load_item4)
    # db.session.add(load_item5)
    # db.session.add(load_item6)

    # Validate load items
    load1.validate_load_items()
    load2.validate_load_items()
    # load3.validate_load_items()

    # Assign the carrier to the load after validating the load items
    load1.carrier = carrier1
    load2.carrier = carrier2
    # load3.carrier = carrier3

    # Insert harvest
    crop1 = Crop(produce_item=banana, carrier=carrier1, quantity=200, harvest_date=date(2023, 1, 15),farmer='Farmer Joe', location='Farmville')
    db.session.add(crop1)

    print("Dados inseridos com sucesso.")

# Call the function to insert the data
if __name__ == "__main__":
    with app.app_context():
        insert_data()
