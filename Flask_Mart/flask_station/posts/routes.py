from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_station import db
from flask_station.models import Post
from flask_station.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(selling_item=form.title.data, price=form.content.data, merchant=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Item', 
                           form=form, legend='New Item')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.merchant != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.selling_item = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Item has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.selling_item
        form.content.data = post.price
    return render_template('create_post.html', title='Update Item',
                           form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.merchant != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Item has been deleted!', 'success')
    return redirect(url_for('main.home'))
