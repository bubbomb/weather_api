import pytest
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
    response = client.get("/weather?long=1")
    print(response.__dict__)
    assert response.status_code == 400
    assert b'missing lat parameter' in response.data

def test_needs_long(client):
    response = client.get("/weather?lat=1")
    print(response.__dict__)
    assert response.status_code == 400
    assert b'missing lon parameter' in response.data

def test_missing_both(client):
    response = client.get("/weather")
    print(response.__dict__)
    assert response.status_code == 400
    assert b'missing lon and lat parameters' in response.data

def test_has_lat_and_long(client):
    response = client.get("/weather?lat=1&long=2")
    print(response.__dict__)
    assert response.status_code == 200