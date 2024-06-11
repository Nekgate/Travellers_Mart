from flask import render_template, request, redirect, url_for, Blueprint
from flask_station.models import Post

# Create a Blueprint named 'main'
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    """
    Home page route that displays a paginated list of posts.

    Retrieves the current page number from the query parameters.
    Fetches posts from the database, ordered by the date they were posted in descending order.
    Paginates the posts to display 5 posts per page.
    Renders the 'home.html' template with the paginated posts.
    """
    # Get the current page number from the query parameters, defaulting to page 1
    page = request.args.get('page', 1, type=int)
    # Query posts from the database, ordered by date posted in descending order, and paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # Render the 'home.html' template with the paginated posts
    return render_template('home.html', posts=posts)

@main.route('/buy')
def buy():
    """
    Redirects the user to the home page when they navigate to the '/buy' route.
    """
    return redirect(url_for('main.home'))

@main.route('/sell')
def sell():
    """
    Redirects the user to the home page when they navigate to the '/sell' route.
    """
    return redirect(url_for('main.home'))

@main.route('/search')
def search():
    """
    Renders the 'search.html' template when the user navigates to the '/search' route.
    """
    return render_template('search.html')

@main.route('/support')
def support():
    """
    Renders the 'support.html' template when the user navigates to the '/support' route.
    """
    return render_template('support.html')

@main.route('/about')
def about():
    """
    Renders the 'about.html' template with the title 'About' when the user navigates to the '/about' route.
    """
    return render_template('about.html', title='About')
