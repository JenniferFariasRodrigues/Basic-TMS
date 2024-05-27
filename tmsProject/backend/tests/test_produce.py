import pytest
from app import create_app, db
from app.models import ProduceItem

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

def test_create_produce_item(client):
    response = client.post('/produce', json={
        "name": "Apple",
        "unit": "kg",
        "category": "fruit"
    })

    assert response.status_code == 201
    assert response.json['name'] == "Apple"
    assert response.json['unit'] == "kg"
    assert response.json['category'] == "fruit"

def test_list_produce_items(client):
    response = client.get('/produce')
    assert response.status_code == 200
    assert type(response.json) == list

def test_update_produce_item(client):
    produce_item = ProduceItem(name="Apple", unit="kg", category="fruit")
    db.session.add(produce_item)
    db.session.commit()

    response = client.put(f'/produce/{produce_item.id}', json={
        "name": "Banana",
        "unit": "bunch",
        "category": "fruit"
    })

    assert response.status_code == 200
    assert response.json['name'] == "Banana"
    assert response.json['unit'] == "bunch"
    assert response.json['category'] == "fruit"
