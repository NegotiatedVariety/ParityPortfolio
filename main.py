from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import RegistrationForm, LoginForm, PortfolioForm
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_bootstrap import Bootstrap
import json
import forms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'QUWU7Ax94jCsknrT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


Bootstrap(app)
nav = Nav(app)

nav.register_element('top', 'the_nav')


@nav.navigation('the_nav')
def create_nav():
    if 'user' in session:

        user_portfolio = Portfolio.query.filter_by(user_id=session['userID']).order_by(Portfolio.id.desc()).first()
        if user_portfolio is not None:

            return Navbar( 'Parity Portfolio',
                            View('Home', 'home'),
                            View('Dashboard', 'userDashboard'),
                            View('Update Portfolio', 'enter_port'),
                            View('Rebalance Portfolio', 'presets'),
                            View('Logout', 'logout')
            )

        else:

            return Navbar('Parity Portfolio',
                          View('Home', 'home'),
                          View('Update Portfolio', 'enter_port'),
                          View('Logout', 'logout')

            )

    else:
        return Navbar( 'Parity Portfolio',
                        View('Home', 'home'),
                        View('Register', 'register'),
                        View('Login', 'login')
        )



# Creates a User table in database with appropriate columns 
class User(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50), unique=True, nullable=False)
   password = db.Column(db.String(50), nullable=False)

   def __repr__(self):
       return f"User('{self.username}')"

# Creates a Portfolio table in database with appropriate columns
class Portfolio(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   international = db.Column(db.Integer, nullable=False)
   domestic = db.Column(db.Integer, nullable=False)
   bonds = db.Column(db.Integer, nullable=False)
   money_market = db.Column(db.Integer, nullable=False)

   def __repr__(self):
       return f"User('{self.user_id}', '{self.domestic}', '{self.international}', '{self.money_market}', '{self.bonds}')"


with open('presets.json', 'r') as input:
    preset_data = json.load(input)



@app.route('/')
@app.route('/home')
def home(): 
    return render_template('home.html')

@app.route("/presets")
def presets():

    if 'user' not in session:
        flash("You must be logged in to access that page!")
        return redirect(url_for('login'))
    else:
        user_portfolio = Portfolio.query.filter_by(user_id=session['userID']).order_by(Portfolio.id.desc()).first()
        if user_portfolio is None:
            flash("Please Update your Portfolio data first")
            return redirect(url_for('enter_port'))
        return render_template('presets.html', title='Base Data', preset_data = preset_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create instance of a user with info entered from Registration form
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        username = form.username.data
        user_query = User.query.filter_by(username=username).first()
        session['user'] = user_query.username
        session['userID'] = user_query.id
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/enterport', methods=['GET', 'POST'])
def enter_port():
    form = PortfolioForm()
    if request.method == "GET":
        if 'user' in session:
            return render_template('userportfolio.html', title='Portfolio', form=form)
        else:
            flash("You must be logged in to access that page!")
            return redirect(url_for('login'))
    else:    
        if form.validate_on_submit():
            # create instance of a portfolio info with info entered from form
            data = Portfolio(user_id=session['userID'], domestic=form.domestic.data, 
            international=form.international.data, money_market=form.money_market.data, bonds=form.bonds.data)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('userDashboard'))


@app.route('/results', methods=['GET', 'POST'])
def results():

    user_portfolio = Portfolio.query.filter_by(user_id=session['userID']).order_by(Portfolio.id.desc()).first()
    selected_preset = preset_data[int(request.form['preset-btn'])]
    preset_name = selected_preset['preset_name']

    domestic = user_portfolio.domestic
    international = user_portfolio.international
    bonds = user_portfolio.bonds
    money_market = user_portfolio.money_market
    current_investments_col = [domestic, international, bonds, money_market]

    total_investments = sum(current_investments_col)

    # Calculate current percentages
    percent_domestic = domestic / total_investments * 100
    percent_international = international / total_investments * 100
    percent_bonds = bonds / total_investments * 100
    percent_money_market = money_market / total_investments * 100

    # Determine target percentages
    target_domestic_percent = selected_preset['domestic_stock']
    target_international_percent = selected_preset['international_stock']
    target_bonds_percent = selected_preset['bonds']
    target_money_market_percent = selected_preset['money_market']

    # Calculate target investments
    target_domestic_investment = target_domestic_percent / 100 * total_investments
    target_international_investment = target_international_percent / 100 * total_investments
    target_bonds_investment = target_bonds_percent / 100 * total_investments
    target_money_market_investment = target_money_market_percent / 100 * total_investments

    # Calculate rebalance $ amount
    cash_diff_domestic = target_domestic_investment - domestic
    cash_diff_international = target_international_investment - international
    cash_diff_bonds = target_bonds_investment - bonds
    cash_diff_money_market = target_money_market_investment - money_market

    # Calculate rebalance %
    percent_diff_domestic = target_domestic_percent - percent_domestic
    percent_diff_international = target_international_percent - percent_international
    percent_diff_bonds = target_bonds_percent - percent_bonds
    percent_diff_money_market = target_money_market_percent - percent_money_market

    # Create columns
    categories_col = ["Domestic Stock", "International Stock", "Bonds", "Money Market"]
    current_percentage_col = [percent_domestic, percent_international, percent_bonds, percent_money_market]
    target_investment_col = [target_domestic_investment, target_international_investment, target_bonds_investment,
                             target_money_market_investment]
    target_percentage_col = [target_domestic_percent, target_international_percent, target_bonds_percent,
                             target_money_market_percent]
    cash_diff_col = [cash_diff_domestic, cash_diff_international, cash_diff_bonds, cash_diff_money_market]
    percent_diff_col = [percent_diff_domestic, percent_diff_international, percent_diff_bonds,
                        percent_diff_money_market]

    # Format output columns
    current_investments_col = ['$' + '{:,.2f}'.format(round(x, 2)) for x in current_investments_col]
    current_percentage_col = ['{:,.2f}'.format(round(x, 2)) + '%' for x in current_percentage_col]
    target_investment_col = ['$' + '{:,.2f}'.format(round(x, 2)) for x in target_investment_col]
    target_percentage_col = ['{:,.2f}'.format(round(x, 2)) + '%' for x in target_percentage_col]
    cash_diff_col = ['+$' + '{:,.2f}'.format(round(x, 2)) if x > 0 else '$' + '{:,.2f}'.format(
        round(x, 2)) if x == 0 else '-$' + '{:,.2f}'.format(round(abs(x), 2)) for x in cash_diff_col]
    percent_diff_col = ['+' + '{:,.2f}'.format(round(x, 2)) + '%' if x > 0 else '{:,.2f}'.format(
        round(x, 2)) + '%' if x == 0 else '-' + '{:,.2f}'.format(round(abs(x), 2)) + '%' for x in percent_diff_col]

    output = [categories_col, current_investments_col, current_percentage_col, target_investment_col,
              target_percentage_col, cash_diff_col, percent_diff_col]

    return render_template('results.html', title='Results', data=output, preset_name=preset_name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()

    if request.method == "GET":
        # user already logged in, redirect to dashboard
        if "user" in session:
            flash("Already logged in!", "success")
            return redirect(url_for("userDashboard"))
        # user must login, redirected to login
        return render_template('login.html', form = form)
    
    elif request.method == "POST" and form.validate_on_submit():
        user = request.form['username']
        password = request.form['password']
        user_query = User.query.filter_by(username=user).first()

        # username not in db
        if user_query is None:
            flash("Username invalid, please register or try again", "error")
            return render_template('login.html', form = form)
        
        # password for user was incorrect
        elif user_query.password != password:
            flash("Invalid Login", "error")
            return render_template('login.html', form = form)
        
        # login successful
        else:
            session.clear()
            session['user'] = user_query.username
            session['userID'] = user_query.id
            user_portfolio = Portfolio.query.filter_by(user_id=session['userID']).order_by(Portfolio.id.desc()).first()
            if user_portfolio is None:
                return redirect(url_for('home'))
            return redirect(url_for('userDashboard'))


@app.route('/userDashboard')
def userDashboard():
    if 'user' in session:
        user = session['user']
        userID = session['userID']
        user_portfolio = Portfolio.query.filter_by(user_id=session['userID']).order_by(Portfolio.id.desc()).first()
        if user_portfolio is None:
            flash("Please Update your Portfolio data first")
            return redirect(url_for('home'))

        
        labels = ["Domestic", "International", "Bonds", "Money Market"]
        values = [user_portfolio.domestic, user_portfolio.international, user_portfolio.bonds, user_portfolio.money_market]
        total = [sum(values)]
        return render_template('userDashboard.html', user = user, labels = labels, values = values, total = total)
    else:
        return NotLoggedIn()



@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for('home'))


def NotLoggedIn():
    flash("Please login or register")
    return redirect(url_for('home'))

# run on debug mode to not re-start server after changes
if __name__ == '__main__':

    app.run(debug = True)
