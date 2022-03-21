from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import News
from forms.user import RegisterForm


a = input()
global_init(a)
db_sess = create_session()
for user in db_sess.query(User).filter(User.address == "module_1", User.position.notin_(["engineer"]),
                                       User.speciality.notin_(["engineer"])):
    print(f"<Colonist> {user.id} {user.surname} {user.name}")