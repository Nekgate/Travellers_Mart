from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify, flash
from flask_station.models import Post, CartItem
from sqlalchemy import func
from flask import send_from_directory
from flask_station import db
from flask_login import current_user, login_required
from flask_station.products.forms import ProductForm

# from flask_station.search.forms import (SearchForm)


main = Blueprint('main', __name__)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@main.route('/products')
def all_product():
    page = request.args.get('page', 1, type=int)
    # Query posts from the database, ordered by date posted in descending order, and paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    for post in posts.items:
        print(post.image)
    return render_template('home.html', posts=posts)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home')
def home():
    # return render_template('home.html', posts=posts)
    # form = SearchForm()
    """
    Home page route that displays a paginated list of posts.

    Retrieves the current page number from the query parameters.
    Fetches posts from the database, ordered by the date they were posted in descending order.
    Paginates the posts to display 5 posts per page.
    Renders the 'home.html' template with the paginated posts.
    """
    query = ""
    result = Post.query.order_by(Post.date_posted.desc()).paginate(page=1, per_page=5)
    if request.method == 'POST' and "search" in request.form:
        query = request.form['search']
        if (query):
             lw = query.lower()
            #  print(Post.query)
             
             result = Post.query.filter(
                 func.lower(Post.selling_item).contains(lw) | 
                 func.lower(Post.content).contains(lw)
                 ).order_by(Post.date_posted.desc()).all()
             print(result)
             
             for post in result:
                print(f"ID: {post.image}, Title: {post.selling_item}, Content: {post.content}, Date Posted: {post.date_posted}")
    return render_template('index.html', query=query, result=result)



@main.route('/buy')
def buy():
    """
    Redirects the user to the home page when they navigate to the '/buy' route.
    """
    return redirect(url_for('main.home'))


# @main.route('/sell')
# def sell():
#     form = ProductForm()
#     if form.validate_on_submit():
#         image = form.image.data
#         filename = image.filename
#         uploads_dir =  'flask_station/static/uploads'
#         print(uploads_dir)
#         os.makedirs(uploads_dir, exist_ok=True)
#         image.save(os.path.join(os.getcwd(), uploads_dir, filename)) 

#         post = Post(selling_item=form.title.data, content=form.content.data, price=form.price.data, image=filename, merchant=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your Post has been updated!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_post.html', title='New Item', 
#                            form=form, legend='New Item')


# @main.route('/search')
# def search():
#     return render_template('search.html')

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

@main.route('/search', methods=['GET', 'POST'])
def search():
    query = ""
    result = []
    if request.method == 'POST':
        query = request.form['search_form']
        print(query)
        if (query):
             lw = query.lower()
            #  print(Post.query)
             
             result = Post.query.filter(
                 func.lower(Post.selling_item).contains(lw) | 
                 func.lower(Post.content).contains(lw)
                 ).order_by(Post.date_posted.desc()).all()
             for post in result:
                print(f"ID: {post.image}, Title: {post.selling_item}, Content: {post.content}, Date Posted: {post.date_posted}")
    return render_template('search.html', query=query, result=result)


@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    response_data = {'success': True, 'product_id': product_id}
    return jsonify(response_data), 200 

@main.route('/cart')
def cart():
    cart = session.get('cart', {})
    products = Post.query.filter(Post.id.in_(cart.keys())).all()
    return render_template('cart.html', cart=cart, products=products)

@main.route('/cart_items', methods=['GET'])
@login_required
def get_cart_items():
    if current_user.id is None:
        flash("Login is required")
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    cart_data = []

    for item in cart_items:
        product = Post.query.get(item.product_id)
        cart_data.append({
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'title': product.selling_item,
            'image': product.image,
        })

    return jsonify(cart_data)