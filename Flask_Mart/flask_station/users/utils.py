import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_station import mail

def save_picture(form_picture):
    """
    Save a profile picture uploaded by the user.

    Args:
        form_picture (FileStorage): The uploaded picture file.

    Returns:
        str: The filename of the saved picture.
    """
    # Generate a random hex string for the filename
    random_hex = secrets.token_hex(8)
    # Extract the file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # Create the final filename
    picture_fn = random_hex + f_ext
    # Determine the path to save the picture
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image to a 125x125 pixel thumbnail
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Save the image to the determined path
    i.save(picture_path)
    return picture_fn

def save_post_picture(form_picture):
    """
    Save a picture uploaded for a post.

    Args:
        form_picture (FileStorage): The uploaded picture file.

    Returns:
        str: The filename of the saved picture.
    """
    # Generate a random hex string for the filename
    random_hex = secrets.token_hex(8)
    # Extract the file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # Create the final filename
    picture_fn = random_hex + f_ext
    # Determine the path to save the picture
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    # Debugging print statement
    print(f"Saving image to: {picture_path}")

    # Resize the image to a 300x300 pixel thumbnail
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Save the image to the determined path
    i.save(picture_path)

    # Confirm the image is saved
    if os.path.exists(picture_path):
        print(f"Image saved successfully at {picture_path}")
    else:
        print(f"Failed to save image at {picture_path}")

    return picture_fn

def send_reset_email(user):
    """
    Send a password reset email to the user.

    Args:
        user (User): The user who requested the password reset.
    """
    # Generate a reset token for the user
    token = user.get_reset_token()
    # Create the email message
    msg = Message('Password Reset Request',
                  sender='noreply@travellersmart.tech',
                  recipients=[user.email])
    # Define the body of the email
    msg.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this message and no changes will be made.
'''
    # Send the email
    mail.send(msg)
