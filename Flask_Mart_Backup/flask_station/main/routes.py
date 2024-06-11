from flask import render_template, request, redirect, url_for, Blueprint
from flask_station.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/buy')
def buy():
    return redirect(url_for('main.home'))


@main.route('/sell')
def sell():
    return redirect(url_for('main.home'))


@main.route('/search')
def search():
    return render_template('search.html')


@main.route('/support')
def support():
    return render_template('support.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')
