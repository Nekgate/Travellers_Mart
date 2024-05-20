from flask import render_template, url_for, flash, redirect
from flask_station import app
from flask_station.forms import RegistrationForm, LoginForm
from flask_station.models import User, Post


descrip = [
    {
        'description': 'Welcome to TravellersMart. This web application aims to provide travellers and foreigners with a seamless platform to purchase a wide range of items, from meals to essentials, in unfamiliar locations, regardless of language barriers. This initiative addresses common travel obstacles by offering a user-friendly solution to efficiently meet their needs.'
    }
]

welcome = [
    {
        'greet': 'Welcome to Travellers Mart',
        'find': 'Feel free to search for your desired items'
    }
]

posts = [
    {
        'merchant': 'Benedict Nathaniel',
        'selling_item': 'Wrist Watch',
        'price': 'Price $500',
        'date_posted': 'April 6th, 2024'
    },
    {
        'merchant': 'Richard Bonk',
        'selling_item': 'Quality Glass',
        'price': 'Price $200',
        'date_posted': 'April 4th, 2024'
    }
]
look = [
    {
        'check': 'Coming Soon!',
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', welcome=welcome)


@app.route('/buy')
def buy():
    return render_template('buy.html', posts=posts)


@app.route('/sell')
def sell():
    return redirect(url_for('buy'))


@app.route('/search')
def search():
    return render_template('search.html', look=look)


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About', descrip=descrip)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You Have Been Logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password' 'danger')
    return render_template('login.html', title='Login', form=form)
