from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_station import db
from flask_station.models import Post
from flask_station.posts.forms import PostForm
from flask_station.users.utils import save_post_picture

# Create a Blueprint named 'posts' to group related routes and views
posts = Blueprint('posts', __name__)

# Route for creating a new post
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Check if a file was uploaded
        if form.image.data:
            # Pass the file object to the save_post_picture function to handle saving
            picture_file = save_post_picture(form.image.data)
        else:
            # If no file was uploaded, use a default image or handle it according to your application logic
            picture_file = 'default.jpg'
        
        # Create a new Post object with the form data and current user as the merchant
        post = Post(selling_item=form.title.data, content=form.content.data, 
                    price=form.price.data, image=picture_file, merchant=current_user)
        db.session.add(post)  # Add the post to the session
        db.session.commit()  # Commit the session to the database
        flash('Your post has been created!', 'success')  # Flash a success message
        return redirect(url_for('main.home'))  # Redirect to the home page
    return render_template('create_post.html', title='New Item', 
                           form=form, legend='New Item')  # Render the form for creating a new post

# Route for viewing a specific post
@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID or return 404 if not found
    return render_template('post.html', title='post.title', post=post)  # Render the post view template

# Route for updating a post
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in before accessing this route
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID or return 404 if not found
    if post.merchant != current_user:  # Ensure the current user is the owner of the post
        abort(403)  # Return 403 Forbidden if not authorized
    form = PostForm()
    if form.validate_on_submit():
        post.selling_item = form.title.data  # Update the post's title
        post.content = form.content.data  # Update the post's content
        post.price = form.price.data  # Update the post's price
        if form.image.data:  # Check if a new image was uploaded
            picture_file = save_post_picture(form.image.data)  # Save the new image
            post.image = picture_file  # Update the post's image
        db.session.commit()  # Commit the changes to the database
        flash('Your Item has been updated!', 'success')  # Flash a success message
        return redirect(url_for('posts.post', post_id=post.id))  # Redirect to the updated post view
    elif request.method == 'GET':
        form.title.data = post.selling_item  # Pre-fill the form with the current post title
        form.content.data = post.content  # Pre-fill the form with the current post content
        form.price.data = post.price  # Pre-fill the form with the current post price
    return render_template('create_post.html', title='Update Item',
                           form=form, legend='Update Post')  # Render the form for updating the post

# Route for deleting a post
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # Get the post by ID or return 404 if not found
    if post.merchant != current_user:  # Ensure the current user is the owner of the post
        abort(403)  # Return 403 Forbidden if not authorized
    db.session.delete(post)  # Delete the post from the session
    db.session.commit()  # Commit the session to the database
    flash('Your Item has been deleted!', 'success')  # Flash a success message
    return redirect(url_for('main.home'))  # Redirect to the home page
