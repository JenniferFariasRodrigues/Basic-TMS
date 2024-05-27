import pytest
from app import create_app, db
from app.models import Carrier

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

def test_responds_400_if_missing_csv(client):
    response = client.post('/carriers/import')
    assert response.status_code == 400
    assert response.json['error'] == 'No file provided'
