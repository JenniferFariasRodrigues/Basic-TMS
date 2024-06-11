from config import db, app
from models import ProduceItem, Carrier, Load, LoadItem, Crop, ValidationError
from transactional import transactional_session
from datetime import date

@transactional_session
def insert_data():
    try:
    
        # Insert product item
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

      

        # Carrier insert
        carrier1 = Carrier(
            name='John Cooper',
            email='johnC@transports.com',
            phone='123412431489',
            company='John Transportes LTDA.',
            address='Flower street, Be nice ranch',
            allowed_items=['banana', 'tomato', 'onion'],  # Adding itens to the list
            max_load_quantity=200  # Maximum quantity  itens
        )
        carrier2 = Carrier(
            name='Mary Smith',
            email='maryS@transports.com',
            phone='3252435146',
            company='Mary Transportes LTDA.',
            address='Tree street, Gold ranch',
            allowed_items=['strawberry', 'blueberries', 'blackberries'],  # Adding itens to the list
            max_load_quantity=100  # Maximum quantity  itens
        )

        carrier3 = Carrier(
            name='Steve Carter',
            email='steveC@transports.com',
            phone='123412431489',
            company='Steve Transportes LTDA.',
            address='Avocado street, Happy ranch',
            allowed_items=['any'],  # # Adding itens to the list
            max_load_quantity=250  # Maximum quantity itens
        )

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.add(carrier3)

        # Load insert
        load1 = Load(customer='Customer A')
        load2 = Load(customer='Customer B')
        load3 = Load(customer='Customer C')

        db.session.add(load1)
        db.session.add(load2)
        db.session.add(load3)

        # Load itens added
        load_item1 = LoadItem(produce_item=banana, quantity=100, load=load1)
        load_item2 = LoadItem(produce_item=tomato, quantity=100, load=load1)
        load_item3 = LoadItem(produce_item=strawberry, quantity=50, load=load2)
        load_item4 = LoadItem(produce_item=blueberries, quantity=50, load=load2)
        load_item6 = LoadItem(produce_item=blueberries, quantity=50, load=load3)
        load_item7 = LoadItem(produce_item=banana, quantity=100, load=load3)
        load_item8 = LoadItem(produce_item=strawberry, quantity=100, load=load3)

        db.session.add(load_item1)
        db.session.add(load_item2)
        db.session.add(load_item3)
        db.session.add(load_item4)
        db.session.add(load_item6)
        db.session.add(load_item7)
        db.session.add(load_item8)

        # Load validation
        load1.validate_load_items()
        load2.validate_load_items()
        load3.validate_load_items()

        # Assign carrier to load after validating load items
        load1.carrier = carrier1
        load2.carrier = carrier2
        load3.carrier = carrier3

        # Harvest insert
        crop1 = Crop(produce_item=banana, carrier=carrier1, quantity=200, harvest_date=date(2023, 1, 15), farmer='Farmer Joe', location='Farmville Blumenau')
        db.session.add(crop1)

        print("Data entered successfully!")
    except Exception as e:
        print(f"Error when entering data: {e}")

if __name__ == "__main__":
    with app.app_context():
        insert_data()
# old3
# def insert_data():
#     try:
#         # ProduceItem insert data
#         produce_items = [
#             ProduceItem(name='Apple', unit='Box', category='Fruit'),
#             ProduceItem(name='Banana', unit='Box', category='Fruit'),
#             ProduceItem(name='Carrot', unit='Bag', category='Vegetable'),
#             ProduceItem(name='Broccoli', unit='Box', category='Vegetable'),
#         ]
#         db.session.add_all(produce_items)
#         db.session.commit()

#         # Carrier insert data
#         carriers = [
#             Carrier(name='Jhon Smith', email='jhon@gmail.com', phone='12417890', company='Jhon Transports', address='123 Avocado St', allowed_items=['Apple', 'Banana'], max_load_quantity=100),
#             Carrier(name='Mry cooper', email='mary@hotmail.com', phone='932104345', company='Mary transports', address='456 Flowers St', allowed_items=['Carrot', 'Broccoli'], max_load_quantity=150),
#         ]
#         db.session.add_all(carriers)
#         db.session.commit()
#         print("Data entered successfully.")

#     except Exception as e:
#         print(f"Error when entering data: {e}")

# if __name__ == "__main__":
#     with app.app_context():
#         insert_data()

# old2
# from config import db, app
# from models import ProduceItem, Carrier, Load, LoadItem, Crop
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.exc import IntegrityError
# from datetime import date

# # Used to manage transactions
# # 
# # Create a scoped session to manage transactions
# # session_factory = sessionmaker(bind=db.engine)
# # Session = scoped_session(session_factory)

# def insert_data():
#     with app.app_context():
#         session_factory = sessionmaker(bind=db.engine)
#         Session = scoped_session(session_factory)
#         session = Session()

#         try:
#             # Insert production items
#             banana = ProduceItem(name='banana', unit='Box', category='fruit')
#             tomato = ProduceItem(name='tomato', unit='Box', category='fruit')
#             onion = ProduceItem(name='onion', unit='Box', category='fruit')
#             melon = ProduceItem(name='melon', unit='Box', category='fruit')
#             strawberry = ProduceItem(name='strawberry', unit='Box', category='fruit')
#             blueberries = ProduceItem(name='blueberries', unit='Box', category='fruit')
#             blackberries = ProduceItem(name='blackberries', unit='Box', category='fruit')

#             session.add(banana)
#             session.add(tomato)
#             session.add(onion)
#             session.add(melon)
#             session.add(strawberry)
#             session.add(blueberries)
#             session.add(blackberries)
#             session.commit()  # Commit to generate IDs for ProduceItems

#             # Insert carrier
#             carrier1 = Carrier(
#                 name='John Smith cooper',
#                 email='j@trans.com.br',
#                 phone='+148988991122',
#                 company='John Transportes LTDA.',
#                 address='Flowers Street, Happy Ranch',
#                 allowed_items=['banana', 'tomato', 'onion'],
#                 max_load_quantity=200
#             )
#             carrier2 = Carrier(
#                 name='Mary Cooper Smith',
#                 email='marycCooper@trans.com',
#                 phone='+233252435147',    
#                 company='Mary Transports LTDA.',
#                 address='Tree Street, North Ranch',
#                 allowed_items=['strawberry', 'blueberries', 'blackberries'],
#                 max_load_quantity=200
#             )
            
#             carrier3 = Carrier(
#                 name='Steve Jobs Smith',
#                 email='steve@trans.com',
#                 phone='+3312431488',
#                 company='Steve Transport LTDA.',
#                 address='Avocado street, Happy Ranch',
#                 allowed_items=['any'],  # Adding the list of allowed items
#                 max_load_quantity=250  # Setting the maximum quantity of items
#             )

#             # session.add(carrier1)
#             # session.add(carrier2)
#             # session.add(carrier3)
#             # session.commit()  # Commit to generate IDs for Carriers

#             # verification to avoid duplicate email addresses
#             for carrier in [carrier1, carrier2, carrier3]:
#                 try:
#                     session.add(carrier)
#                     session.commit()
#                 except IntegrityError:
#                     session.rollback()
#                     print(f"Email address '{carrier.email}' already exists. Omitting carrier insertion.")           
#                     # Carrier Insert
#             load1 = Load(customer='Customer A')
#             load2 = Load(customer='Customer B')
#             load3 = Load(customer='Customer C')

#             session.add(load1)
#             session.add(load2)
#             session.add(load3)
#             session.commit()  # Commit to generate IDs for Loads

#             # Insert items into the load.
#             load_item1 = LoadItem(produce_item=banana, quantity=100, load=load1)
#             load_item2 = LoadItem(produce_item=tomato, quantity=100, load=load1)
#             load_item3 = LoadItem(produce_item=strawberry, quantity=50, load=load2)
#             load_item4 = LoadItem(produce_item=blueberries, quantity=50, load=load2)
#             load_item5 = LoadItem(produce_item=blueberries, quantity=50, load=load3)
#             load_item6 = LoadItem(produce_item=banana, quantity=100, load=load3)
#             load_item7 = LoadItem(produce_item=strawberry, quantity=100, load=load3)

#             session.add(load_item1)
#             session.add(load_item2)
#             session.add(load_item3)
#             session.add(load_item4)
#             session.add(load_item5)
#             session.add(load_item6)
#             session.add(load_item7)
#             session.commit()  # Commit to generate IDs for LoadItems

#             # Validate load items
#             load1.validate_load_items()
#             load2.validate_load_items()
#             load3.validate_load_items()

#             # Assign the carrier to the load after validating the load items
#             load1.carrier = carrier1
#             load2.carrier = carrier2
#             load3.carrier = carrier3 
#             session.add(load1)
#             session.add(load2)
#             session.add(load3)
#             session.commit()

#             # Insert harvest
#             crop1 = Crop(produce_item=banana, carrier=carrier1, quantity=200, harvest_date=date(2023, 1, 15), farmer='Farmer Joe', location='Blumenau')
#             session.add(crop1)

#             # Commit the transaction
#             session.commit()
#             print("Data entered successfully.")

#         except Exception as e:
#             # Rollback in case of error
#             session.rollback()
#             print(f"Error when entering data: {e}")
#         finally:
#             # Close the session
#             session.close()

# # Call the function to insert the data
# if __name__ == "__main__":
#     with app.app_context():
#         insert_data()
        
        
        

# Old code
# def insert_data():
#     # Insert production items
#     banana = ProduceItem(name='banana', unit='Box', category='fruit')
#     tomato = ProduceItem(name='tomato', unit='Box', category='fruit')
#     onion = ProduceItem(name='onion', unit='Box', category='fruit')
#     melon = ProduceItem(name='melon', unit='Box', category='fruit')
#     strawberry = ProduceItem(name='strawberry', unit='Box', category='fruit')
#     blueberries = ProduceItem(name='blueberries', unit='Box', category='fruit')
#     blackberries = ProduceItem(name='blackberries', unit='Box', category='fruit')

#     db.session.add(banana)
#     db.session.add(tomato)
#     db.session.add(onion)
#     db.session.add(melon)
#     db.session.add(strawberry)
#     db.session.add(blueberries)
#     db.session.add(blackberries)

#     # Insert carrier
#     carrier1 = Carrier(
#         name='John',
#         email='john@transports.com',
#         phone='+5548988991122',
#         company='John Transportes LTDA.',
#         address='Flowers Street, Happy Ranch',
#         allowed_items=['banana', 'tomato', 'onion'],  # Adding the list of allowed items
#         max_load_quantity=200  # Setting the maximum quantity of items
#     )
#     carrier2 = Carrier(
#         name='Mary',
#         email='mary@transports.com',
#         phone='+55533252435146',
#         company='Mary Transportes LTDA.',
#         address='Tree Street., North Ranch',
#         allowed_items=['strawberry', 'blueberries', 'amoras'],  # Adding the list of allowed items
#         max_load_quantity=100  # Setting the maximum quantity of items
#     )

#     # carrier3 = Carrier(
#     #     name='Steve',
#     #     email='steve@transports.com',
#     #     phone='123412431489',
#     #     company='Steve Transportes LTDA.',
#     #     address='Rua do abacate, Rancho feliz',
#     #     allowed_items=[],  # Adicionando a lista de itens permitidos
#     #     max_load_quantity=250  # Definindo a quantidade máxima de itens
#     # )

#     db.session.add(carrier1)
#     db.session.add(carrier2)
#     # db.session.add(carrier3)

#     # Carrier Insert
#     load1 = Load(customer='Customer A')
#     load2 = Load(customer='Customer B')
#     # load3 = Load(customer='Customer C')

#     db.session.add(load1)
#     db.session.add(load2)
#     # db.session.add(load3)

#     # Insert items into the load.
#     load_item1 = LoadItem(produce_item=banana, quantity=100, load=load1)
#     load_item2 = LoadItem(produce_item=tomato, quantity=100, load=load1)
#     load_item3 = LoadItem(produce_item=strawberry, quantity=50, load=load2)
#     load_item4 = LoadItem(produce_item=blueberries, quantity=50, load=load2)
#     # load_item5 = LoadItem(produce_item=banana, quantity=150, load=load3)
#     # load_item6 = LoadItem(produce_item=melao, quantity=150, load=load3)

#     db.session.add(load_item1)
#     db.session.add(load_item2)
#     db.session.add(load_item3)
#     db.session.add(load_item4)
#     # db.session.add(load_item5)
#     # db.session.add(load_item6)

#     # Validate load items
#     load1.validate_load_items()
#     load2.validate_load_items()
#     # load3.validate_load_items()

#     # Assign the carrier to the load after validating the load items
#     load1.carrier = carrier1
#     load2.carrier = carrier2
#     # load3.carrier = carrier3

#     # Insert harvest
#     crop1 = Crop(produce_item=banana, carrier=carrier1, quantity=200, harvest_date=date(2023, 1, 15),farmer='Farmer Joe', location='Farmville')
#     db.session.add(crop1)

#     print("Dados inseridos com sucesso.")

# # Call the function to insert the data
# if __name__ == "__main__":
#     with app.app_context():
#         insert_data()
