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
        long = request.args.get('long')
        if not lat and not long:
            return "missing lon and lat parameters", 400
        elif not lat:
            return "missing lat parameter", 400
        elif not long:
            return "missing lon parameter", 400

        return "", 200

    return app

app = create_app()



#https://api.openweathermap.org/data/2.5/weather?lat=40.363918&lon=-111.738869&appid=c22bc649b8f42935ff334297e177edc5
