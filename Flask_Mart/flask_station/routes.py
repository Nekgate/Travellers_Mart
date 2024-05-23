import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_station import app, db, bcrypt
from flask_station.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_station.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been succesfully created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password' 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
