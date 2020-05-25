import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=ef08b95775e54de3d2f9b294e539fb4e'
    r = requests.get(url).json()
    return r


@app.route('/')
def index_get():
    cities = City.query.all()
    cities = cities[-2:]
    cities = cities[::-1]

    weather_data = []
    i = 0

    for city in cities:

        r = get_weather_data(city.name)
        print(city.name)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)
        i += 1
        if i == 1:
            break

    return render_template('weather.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')

    new_city_data = get_weather_data(new_city)

    if new_city_data['cod'] == 200:
        new_city_obj = City(name=new_city)

        db.session.add(new_city_obj)
        db.session.commit()
    else:
        err_msg = f'City {new_city} does not exist in the world!'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!')

    return redirect(url_for('index_get'))


@app.route('/aboutme', methods=['GET', 'POST'])
def aboutme():
    return render_template('about.html')


@app.route('/showall')
def showall():
    cities = City.query.all()
    cities = cities[::-1]
    li = []
    weather_data = []

    for city in cities:

        r = get_weather_data(city.name)
        print(r)
        if city.name not in li:
            weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }

            weather_data.append(weather)
            li.append(city.name)

    return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
