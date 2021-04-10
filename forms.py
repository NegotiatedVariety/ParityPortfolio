from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, EqualTo, InputRequired, Email
from wtforms.fields.html5 import EmailField

class RegistrationForm(FlaskForm):
    username =StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(), 
        Length(min=5, max=15, message="Username must be between 5 and 15 characters long.")])
    password = PasswordField("Password", validators=[InputRequired()]) 
    submit = SubmitField("Login")


class PortfolioForm(FlaskForm):
    international = StringField('$', validators=[DataRequired()])
    domestic = StringField('$', validators=[DataRequired()])
    money_market = StringField('$', validators=[DataRequired()])
    bonds = StringField('$', validators=[DataRequired()])
    submit = SubmitField('Submit Portfolio')

