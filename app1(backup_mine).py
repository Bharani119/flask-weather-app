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


@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ef08b95775e54de3d2f9b294e539fb4e'
    err_msg=''
    if request.method == 'POST':
        new_city = request.form.get('city')
        r = requests.get(url.format(new_city)).json()
        if r['cod'] == 200:
            if new_city:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
        else:
            err_msg = "The entered city is not in the World"
            print(err_msg)

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!')

    cities = City.query.all()
    # print(cities[-2:])
    cities = cities[-2:]
    cities = cities[::-1]

    # delete this

    # city = 'chennai'
    # r = requests.get(url.format(city)).json()

    # weather = {
    #     'city': city,
    #     'temperature': r['main']['temp'],
    #     'description': r['weather'][0]['description'],
    #     'icon': r['weather'][0]['icon'],
    # }
    # print(weather)
    # weather_data = []
    # weather_data.append(weather)

    # upto this delete

    weather_data = []
    i = 0
    for city in cities:

        r = requests.get(url.format(city.name)).json()
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
    # return render_template('weather.html')


@app.route('/aboutme', methods=['GET', 'POST'])
def aboutme():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
