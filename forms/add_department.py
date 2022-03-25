import sqlalchemy
import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired


class AddDepartment(FlaskForm):
    title = StringField("Title of department", validators=[DataRequired()])
    chef = StringField("Chef (name surname)", validators=[DataRequired()])
    members = StringField("Members (1, 2, ...)", validators=[DataRequired()])
    department_email = EmailField("Department email", validators=[DataRequired()])
    submit = SubmitField("Submit")