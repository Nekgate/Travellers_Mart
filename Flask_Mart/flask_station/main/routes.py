from flask import render_template, request, redirect, url_for, Blueprint, session, jsonify, flash
from flask_station.models import Post, CartItem
from sqlalchemy import func
from flask_station import db
from flask_login import current_user, login_required



main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home')
def home():
    """
    Home page route that displays a paginated list of posts.

    Retrieves the current page number from the query parameters.
    Fetches posts from the database, ordered by the date they were posted in descending order.
    Paginates the posts to display 5 posts per page.
    Renders the 'home.html' template with the paginated posts.
    """
    query = ""
    page = request.args.get('page', 1, type=int)
    result = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if request.method == 'POST' and "search" in request.form:
        query = request.form['search']
        if (query):
             lw = query.lower()
            #  print(Post.query)
             
             result = Post.query.filter(
                 func.lower(Post.selling_item).contains(lw) | 
                 func.lower(Post.content).contains(lw)
                 ).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
    flash("Product has been added to cart", 'success')
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
    cart_items = CartItem.query.filter_by(user_id=current_user.id).order_by((CartItem.last_modified.desc())).all()
    cart_data = []

    for item in cart_items:
        product = Post.query.get(item.product_id)
        if product:
             cart_data.append({
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'title': product.selling_item,
            'image': product.image,
            'price': product.price,

        })

    return jsonify(cart_data)

@main.route('/increase_quantity/<int:product_id>', methods=['POST'])
@login_required
def increase_quantity(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404

@main.route('/decrease_quantity/<int:product_id>', methods=['POST'])
@login_required
def decrease_quantity(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            # If quantity is already 1, remove the item from the cart
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Item removed from cart'}), 200
    else:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404

@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Item removed from cart'}), 200
    else:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404
    


@main.route('/products')
def all_product():
    page = request.args.get('page', 1, type=int)
    # Query posts from the database, ordered by date posted in descending order, and paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)
