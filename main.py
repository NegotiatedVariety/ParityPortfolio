from flask import Flask, render_template, url_for, redirect 
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
import json
import forms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'QUWU7Ax94jCsknrT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50), unique=True, nullable=False)
   password = db.Column(db.String(50), nullable=False)

   def __repr__(self):
       return f"User('{self.username}')"



with open('presets.json', 'r') as input:
    preset_data = json.load(input)

@app.route('/')
@app.route('/home')
def home(): 
    return render_template('home.html')

@app.route("/presets")
def presets():
    return render_template('presets.html', title='Base Data', preset_data = preset_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect('userDashboard')
    return render_template('login.html', form = form)

@app.route('/userDashboard')
def userDashboard():
    return render_template('userDashboard.html')


# run on debug mode to not re-start server after changes
if __name__ == '__main__':

    app.run(debug = True)
