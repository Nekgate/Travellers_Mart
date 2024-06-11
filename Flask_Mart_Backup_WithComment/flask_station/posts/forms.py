from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

# Define the PostForm class, which inherits from FlaskForm
class PostForm(FlaskForm):
    # Title field for the item, requires input from the user
    title = StringField('Item Name', validators=[DataRequired()])
    
    # Content field for the item description, requires input from the user
    content = TextAreaField('Item Description', validators=[DataRequired()])
    
    # Price field for the item, requires input from the user
    price = StringField('Price', validators=[DataRequired()])
    
    # Image field for uploading an image, allows only certain file types
    image = FileField('Image URL', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    # Submit button to post the form
    submit = SubmitField('Post')
