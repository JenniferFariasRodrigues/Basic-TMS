import pytest
from app import create_app, db
from app.models import Carrier

@pytest.fixture
def app():
    app = create_app()
   # Configure the application to use an in-memory SQLite database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # yield to provide the application for testing.
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# The test client is used to simulate HTTP requests to the application during testing.
#Use the test client to make a POST request to the /carriers/import route without sending a CSV file.
#Checks whether the response status is 400 (Bad Request), indicating that the request was unsuccessful due to a missing file.
#Checks whether the JSON response contains the 'No file provided' error message.
def test_responds_400_if_missing_csv(client):
    response = client.post('/carriers/import')
    assert response.status_code == 400
    assert response.json['error'] == 'No file provided'
