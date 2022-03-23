from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import News
from forms.user import RegisterForm
import sqlalchemy


a = input()
global_init(a)
db_sess = create_session()
team_leads = []
for job1 in db_sess.query(Jobs).all():
    team_leads.append([db_sess.query(User).filter(User.id == job1).first(), job1.team_leader])

