from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from __init__.forms import RegisterForm, LoginForm, NewFilmForm, FilterForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.app_context().push()


login.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    url = db.Column(db.String)
    id_poster = db.Column(db.Integer)
    id_genre = db.Column(db.Integer)
    id_country = db.Column(db.Integer)
    min_year = db.Column(db.Integer)
    max_year = db.Column(db.Integer)


errors = ('This name already used', "You must be poster this film", "Choose other genre, example: Action film, "
                    "Adventure film, Animated film, Comedy film, Drama, Fantasy film, Historical film, "
                    "Horror film, Musical film,Noir film, Romance film, Science fiction film, Thriller film, Western")

all_genres = ('Action film', 'Adventure film', 'Animated film', 'Comedy film',
              'Drama', 'Fantasy film', 'Historical film', 'Horror film', 'Musical film',
              'Noir film', 'Romance film', 'Science fiction film', 'Thriller film', 'Western')


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route('/')
def home():
    form = FilterForm()
    return render_template("home.html", form=form, filter=False, title="Home", films=Film.query.all())


@app.route('/filter', methods=["GET", "POST"])
def filter():
    form = FilterForm()
    if form.validate_on_submit():
        films = Film.query.all()
        filter_name = form.name.data
        filter_genre = form.genre.data
        filter_country = form.country.data

        if filter_name != "":
            last_films = films.copy()
            for i in last_films:
                if i.name != filter_name:
                    films.remove(i)

        if filter_genre != "":
            last_films = films.copy()
            if filter_genre in all_genres:
                for i in last_films:
                    if i.id_genre != all_genres.index(filter_genre):
                        films.remove(i)
            else:
                films.clear()
        if filter_country != "":
            filter_country = Country.query.filter_by(name=filter_country).first()
            last_films = films.copy()
            if not filter_country:
                films.clear()
            else:
                for i in last_films:
                    if i.id_country != filter_country.id:
                        films.remove(i)
        return render_template("home.html", form=form, filter=True, title="Home", films=films)

    return render_template("home.html", form=form, filter=True, title="Filter", films=Film.query.all())


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        db.session.add(User(name=name, password=password))
        db.session.commit()
        login_user(User.query.filter_by(name=name).first(), remember=form.remember.data)
        return redirect('/')
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = User.query.filter_by(name=name).first()
        if user is None or user.password != password:
            return redirect('/login')
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return render_template("login.html", form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/film/<int:id>')
def film(id):
    film = Film.query.get(id)
    return render_template("film.html", name=film.name, description=film.description, date=film.date,
                           image=film.image, url=film.url, poster=User.query.get(film.id_poster).name,
                           country=Country.query.get(film.id_country).name, genre=all_genres[film.id_genre])


@login_required
@app.route('/film/<int:id>/delete')
def film_delete(id):
    if current_user.id == Film.query.get(id).id_poster:
        db.session.delete(Film.query.get(id))
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/error/1')


@app.route('/new_film', methods=["GET", "POST"])
@login_required
def new_film():
    form = NewFilmForm()
    if request.method == 'POST':
        file = request.files['image']
        file.save(f'static/images/{file.filename}')
    if form.validate_on_submit():

        name_genre = form.genre.data
        if name_genre in all_genres:

            name_country = form.country.data
            if not Country.query.filter_by(name=name_country).first():
                db.session.add(Country(name=name_country))
                db.session.commit()

            db.session.add(Film(name=form.name.data, description=form.description.data,
                                image=f'static/images/{file.filename}', url=form.url.data, id_poster=current_user.id,
                                id_genre=all_genres.index(name_genre),
                                id_country=Country.query.filter_by(name=name_country).first().id))
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/error/2')

    return render_template("new_film.html", form=form, title="Create new film")


@app.route('/error/<int:id>')
def error(id):
    return render_template("error.html", error=errors[id])
