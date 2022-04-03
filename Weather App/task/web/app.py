import sys
import json
import requests

from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'a2eec5522c1c2c34cdf69f49e448083b'
user_agent = {'User-agent': 'Mozilla/5.0'}


def page_not_found(e):
    return render_template('404.html'), 404


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
            dict_with_weather_info = r.json()
            # TODO add save to file functionality?
            return render_template('index.html', weather=dict_with_weather_info)
        # TODO need to add var "weather" to index HTML
        else:
            return render_template('index.html', weather=None)

            # return render_template('index.html')



# don't change the following way to run flask:
if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)

'''
{
  "base": "stations", 
  "clouds": {
    "all": 11
  }, 
  "cod": 200, 
  "coord": {
    "lat": 53.6884, 
    "lon": 23.8258
  }, 
  "dt": 1648999962, 
  "id": 627904, 
  "main": {
    "feels_like": 272.39, 
    "grnd_level": 993, 
    "humidity": 35, 
    "pressure": 1010, 
    "sea_level": 1010, 
    "temp": 276.08, 
    "temp_max": 276.08, 
    "temp_min": 276.08
  }, 
  "name": "Hrodna", 
  "sys": {
    "country": "BY", 
    "sunrise": 1648958001, 
    "sunset": 1649005342
  }, 
  "timezone": 10800, 
  "visibility": 10000, 
  "weather": [
    {
      "description": "few clouds", 
      "icon": "02d", 
      "id": 801, 
      "main": "Clouds"
    }
  ], 
  "wind": {
    "deg": 329, 
    "gust": 6.69, 
    "speed": 4.12
  }
}'''
