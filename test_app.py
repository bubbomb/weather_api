import pytest
import json
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_default_route(client):
    response = client.get("/")
    assert b"welcome to the weather API, use the /weather endpoint for weather data" in response.data

def test_needs_lat(client):
    response = client.get("/weather?lon=1")
    assert response.status_code == 400
    assert b'missing lat parameter' in response.data

def test_needs_long(client):
    response = client.get("/weather?lat=1")
    assert response.status_code == 400
    assert b'missing lon parameter' in response.data

def test_missing_both(client):
    response = client.get("/weather")
    assert response.status_code == 400
    assert b'missing lon and lat parameters' in response.data

def test_has_lat_and_long(client):
    response = client.get("/weather?lat=1&lon=2")
    assert response.status_code == 200
    response_dict = json.loads(response.data.decode('utf-8') or '{}')
    assert response_dict.get('condition', '') == 'clear sky'
    assert response_dict.get('temperature', '') == 'cold'
