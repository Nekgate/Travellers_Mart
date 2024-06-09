from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Item Name', validators=[DataRequired()])
    content = TextAreaField('Item Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    image = FileField('Image URL', validators = [FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')
