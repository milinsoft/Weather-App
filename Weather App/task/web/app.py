import sys
import requests

from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'a2eec5522c1c2c34cdf69f49e448083b'
user_agent = {'User-agent': 'Mozilla/5.0'}


def page_not_found(e):
    return render_template('404.html'), 404


def convert_to_celcius(kelvin_value: float) -> float:
    return kelvin_value - 273.15


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == "POST":
        city_name = request.form.get('city_name')
        if not city_name:
            return render_template('index.html', weather=None)
        web_site = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
        r = requests.get(web_site, headers=user_agent)

        if r.status_code == 200:
            json_data = r.json()
            dict_with_weather_info = {
                'temp': round(convert_to_celcius(float(json_data['main']['temp']))),
                'state': json_data['weather'][0]['main'],
                'name': json_data['name'],
            }
            # TODO add save to file functionality?
            return render_template('index.html', weather=dict_with_weather_info)
        else:
            return render_template('index.html', weather=None)


# don't change the following way to run flask:
if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
