from test.fixtures import client, app, runner

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
