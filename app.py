import requests
import os
import logging

from flask import Flask
from flask import request


WEATHER_URL_PATTERN = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial'

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def welcome_message():
        return "welcome to the weather API, use the /weather endpoint for weather data"

    @app.route("/weather")
    def weather():
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if not lat and not lon:
            return "missing lon and lat parameters", 400
        elif not lat:
            return "missing lat parameter", 400
        elif not lon:
            return "missing lon parameter", 400

        return get_weather_data_response(lat, lon)

    return app

app = create_app()

def get_weather_data_response(lat, lon):
    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key:
        logging.error('WEATHER_API_KEY not implemented correctly, refer to documentation to set up.')
        return {}, 501

    open_weather_data, status_code = request_open_weather_data(lat, lon, api_key)

    condition = open_weather_data['weather'][0]['description']
    temperature = get_temperature(open_weather_data['main']['feels_like'])
    weather_data = {
        'condition':condition,
        'temperature': temperature,
    }

    return weather_data, status_code

def get_temperature(feels_like):
    if feels_like >= 90:
        return 'hot'
    elif feels_like >= 60:
        return 'moderate'
    return 'cold'

def request_open_weather_data(lat, lon, api_key):
    weather_url = WEATHER_URL_PATTERN.format(lat=lat, lon=lon, api_key=api_key)

    results = requests.get(weather_url)
    json = results.json()
    print(json)
    return json, results.status_code
