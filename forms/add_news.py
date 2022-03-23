import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddNews(FlaskForm):
    title = StringField("Title of news", validators=[DataRequired()])
    about_it = TextAreaField("About the news", validators=[DataRequired()])
    is_private = BooleanField("Is private")
    submit = SubmitField('Submit')