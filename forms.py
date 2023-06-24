from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password Repeat', validators=[EqualTo('password'), DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Enter')


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Enter')


class NewFilmForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Enter')


class FilterForm(FlaskForm):
    name = StringField('Name')
    genre = StringField('Genre')
    country = StringField('Country')
    submit = SubmitField('Enter')