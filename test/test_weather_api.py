import responses
import json

from copy import deepcopy
from test.fixtures import client, app, runner
from app import WEATHER_URL_PATTERN

DEFAULT_RESPONSE = {
        'weather':[{'description':'clear sky'}],
        'main': {
            'feels_like':40
        }
    }

@responses.activate
def test_weather_is_cold(client):

    weather_url = WEATHER_URL_PATTERN.format(lat=1, lon=2, api_key='1234')

    responses.get(
        url = weather_url,
        json= DEFAULT_RESPONSE,
        status=200
    )

    response = client.get("/weather?lat=1&lon=2")
    response_dict = json.loads(response.data.decode('utf-8') or '{}')
    assert response_dict.get('temperature', '') == 'cold'

@responses.activate
def test_weather_is_hot(client):

    response_json = deepcopy(DEFAULT_RESPONSE)
    response_json['main']['feels_like'] = 90
    weather_url = WEATHER_URL_PATTERN.format(lat=1, lon=2, api_key='1234')

    responses.get(
        url = weather_url,
        json= response_json,
        status=200
    )

    response = client.get("/weather?lat=1&lon=2")
    response_dict = json.loads(response.data.decode('utf-8') or '{}')
    assert response_dict.get('temperature', '') == 'hot'

@responses.activate
def test_weather_is_moderate(client):

    response_json = deepcopy(DEFAULT_RESPONSE)
    response_json['main']['feels_like'] = 65
    weather_url = WEATHER_URL_PATTERN.format(lat=1, lon=2, api_key='1234')

    responses.get(
        url = weather_url,
        json= response_json,
        status=200
    )

    response = client.get("/weather?lat=1&lon=2")
    response_dict = json.loads(response.data.decode('utf-8') or '{}')
    assert response_dict.get('temperature', '') == 'moderate'

@responses.activate
def test_weather_is_rainy(client):

    response_json = deepcopy(DEFAULT_RESPONSE)
    response_json['weather'][0]['description'] = 'rainy'
    weather_url = WEATHER_URL_PATTERN.format(lat=1, lon=2, api_key='1234')

    responses.get(
        url = weather_url,
        json= response_json,
        status=200
    )

    response = client.get("/weather?lat=1&lon=2")
    response_dict = json.loads(response.data.decode('utf-8') or '{}')
    assert response_dict.get('condition', '') == 'rainy'