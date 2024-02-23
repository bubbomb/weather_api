from flask import Flask
from flask import request


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
    weather_data ={
        'condition': 'clear sky',
        'temperature': 'cold',
    }
    status_code = 200
    return weather_data, status_code


#https://api.openweathermap.org/data/2.5/weather?lat=40.363918&lon=-111.738869&appid=c22bc649b8f42935ff334297e177edc5
