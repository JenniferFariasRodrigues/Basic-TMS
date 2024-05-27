import pytest
from app import create_app, db
from app.models import Load, Carrier, ProduceItem

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_load(client):
    produce_item = ProduceItem(name="Tomato", unit="kg", category="vegetable")
    db.session.add(produce_item)
    db.session.commit()

    response = client.post('/loads', json={
        "customer": "Customer A",
        "status": "pending",
        "produce_items": [produce_item.id]
    })

    assert response.status_code == 201
    assert response.json['customer'] == "Customer A"
    assert response.json['status'] == "pending"

def test_list_loads(client):
    response = client.get('/loads')
    assert response.status_code == 200
    assert type(response.json) == list

def test_assign_carrier_to_load(client):
    carrier = Carrier(name="Carrier A", email="carrier@example.com", phone="1234567890", company="Company A", address="123 Street")
    db.session.add(carrier)
    db.session.commit()

    load = Load(customer="Customer A", status="pending")
    db.session.add(load)
    db.session.commit()

    response = client.post(f'/loads/{load.id}/assign', json={"carrier_id": carrier.id})

    assert response.status_code == 200
    assert response.json['carrier']['name'] == "Carrier A"
    assert response.json['status'] == "booked"
