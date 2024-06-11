from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_station import db, create_app
from flask_station.models import Post
from flask_station.products.forms import ProductForm
import os
# from run import app
# from flask_station.users.utils import save_picture

posts = Blueprint('products', __name__)


@posts.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_post():
    print()
    form = ProductForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = image.filename
        uploads_dir =  'flask_station/static/uploads'
        print(uploads_dir)
        os.makedirs(uploads_dir, exist_ok=True)
        image.save(os.path.join(os.getcwd(), uploads_dir, filename)) 

        post = Post(selling_item=form.title.data, content=form.content.data, price=form.price.data, image=filename, merchant=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Item', 
                           form=form, legend='New Product')


@posts.route('/product/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


@posts.route('/product/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.merchant != current_user:
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = image.filename
        uploads_dir =  'flask_station/static/uploads'
        print(uploads_dir)
        os.makedirs(uploads_dir, exist_ok=True)
        image.save(os.path.join(os.getcwd(), uploads_dir, filename)) 

        post.selling_item = form.title.data
        post.content = form.content.data
        post.price = form.price.data
        post.image=filename
        db.session.commit()
        flash('Your Item has been updated!', 'success')
        return redirect(url_for('products.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.selling_item
        form.content.data = post.content
        form.price.data = post.price
    return render_template('create_post.html', title='Update Item',
                           form=form, legend='Update Product')


@posts.route('/product/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.merchant != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Item has been deleted!', 'success')
    return redirect(url_for('main.home'))

