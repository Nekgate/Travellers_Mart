import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_station import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    # Debugging print
    print(f"Saving image to: {picture_path}")

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    # Confirm the image is saved
    if os.path.exists(picture_path):
        print(f"Image saved successfully at {picture_path}")
    else:
        print(f"Failed to save image at {picture_path}")

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@travellersmart.tech',
                  recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this message and no changes will be made.
'''
    mail.send(msg)
