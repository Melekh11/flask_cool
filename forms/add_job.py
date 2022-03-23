import sqlalchemy
import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired


class AddJobs(FlaskForm):
    job = StringField("Title of job", validators=[DataRequired()])
    work_size = IntegerField("Work size(hours)", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    start_date = StringField("Start date (dd/mm/yyyy)", validators=[DataRequired()])
    finish_date = StringField("End date (dd/mm/yyyy)", validators=[DataRequired()])
    is_finished = BooleanField("Is finished")
    team_leader_name = StringField("Team leader name", validators=[DataRequired()])
    team_leader_surname = StringField("Team leader surname", validators=[DataRequired()])
    submit = SubmitField("Submit")
