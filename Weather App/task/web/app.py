import sys
from datetime import datetime, timedelta

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)

API_KEY = 'a2eec5522c1c2c34cdf69f49e448083b'
user_agent = {'User-agent': 'Mozilla/5.0'}
DB_NAME = 'weather'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'

db = SQLAlchemy(app)


def get_part_of_the_day(hour: int) -> str:
    if any((5 < hour < 12, 17 < hour < 24)):
        return 'evening-morning'  # for template purposes
    elif 11 < hour < 18:
        return 'day'
    return 'night'


class WeatherDB(db.Model):
    __tablename__ = DB_NAME

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)


# not necessary for now
class EventSchema(Schema):
    id = fields.Integer()
    name = fields.String()


db.create_all()  # save the table in the database


def page_not_found(e):
    return render_template('404.html'), 404


# move to DB method?
def add_to_database(city_name):
    if not city_name:
        pass
    city = WeatherDB(name=city_name)
    db.session.add(city)
    db.session.commit()


def get_weather_from_api(city_name) -> dict:
    def convert_to_celcius(kelvin_value: float) -> int:
        return int(round(kelvin_value - 273.15))

    web_site = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
    r = requests.get(web_site, headers=user_agent)
    if r.status_code == 200:
        json_data = r.json()
        dict_with_weather_info = {
            'temp': convert_to_celcius(float(json_data['main']['temp'])),
            'state': json_data['weather'][0]['main'],
            'name': json_data['name'].upper(),
            'local_time': datetime.utcnow() + timedelta(seconds=int(json_data['timezone'])),
        }
        dict_with_weather_info['day_part'] = get_part_of_the_day(dict_with_weather_info['local_time'].hour)
        # TODO implement sort by part of the day
        return dict_with_weather_info
    return dict()


# use list comprehension?
def get_forecast() -> list:
    cities_in_db = WeatherDB.query.all()
    weather_data: list = []
    for city in cities_in_db:
        data = get_weather_from_api(city.name)
        if data:
            weather_data.append(data)
    return weather_data


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        weather_data = get_forecast()
        return render_template('index.html', cities=weather_data)
    else:
        city_name = request.form.get('city_name')
        add_to_database(city_name)
        return redirect(url_for('index'))  # name of the function


# don't change the following way to run flask:
if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
