from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f41cf22427d898c5451e9acad626160b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='merchant', lazy="dynamic")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selling_item = db.Column(db.String(100), nullable=False,)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.selling_item}', '{self.date_posted}')"


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


if __name__ == '__main__':
    app.run(debug=True)
