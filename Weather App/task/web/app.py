import json

from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)

API_KEY = 'a2eec5522c1c2c34cdf69f49e448083b'
user_agent = {'User-agent': 'Mozilla/5.0'}

def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        city_name = request.form.get('city_name')

        if not city_name:
            return render_template('index.html')

        if city_name:
            with open('static/city.list.json', 'r') as data:
                city_data = [x for x in json.load(data) if city_name.lower() in x['name'].lower()]
                if city_data:
                    city_id = city_data[0]['id']
                    web_site = f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}'
                    r = requests.get(web_site, headers=user_agent)
                    if r.status_code == 200:
                        dict_with_weather_info = json.loads(r.text)
                        # TODO add save to file functionality?
                        return render_template('index.html', weather=dict_with_weather_info)
                        # TODO need to add var "weather" to index HTML
                else:
                    return "This city does not exist!"

        # return render_template('index.html')


# don't change the following way to run flask:
if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
