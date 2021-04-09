from flask import Flask, render_template, url_for
from forms import RegistrationForm
import json

app = Flask(__name__)

with open('presets.json', 'r') as input:
    preset_data = json.load(input)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/presets")
def json_dump():
    return render_template('presets.html', title='Base Data', preset_data = preset_data)

# run on debug mode to not re-start server after changes
if __name__ == '__main__':

    app.run(debug = True)
