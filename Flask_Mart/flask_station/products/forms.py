from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileRequired


class ProductForm(FlaskForm):
    title = StringField('Item Name', validators=[DataRequired()])
    content = TextAreaField('Item Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    # image = FileField('Image URL', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired()])
    # image = FileField('Image URL', validators=[FileRequired(), FileAllowed("png", "jpg")])
    submit = SubmitField('Create Product')
