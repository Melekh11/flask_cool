from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import News
from forms.user import RegisterForm


a = input()
global_init(a)
db_sess = create_session()
arr_leads = []
for user in db_sess.query(User).filter(User.address == "module_1", User.age < 21).all():
    user.address = "module_1"
db_sess.commit()