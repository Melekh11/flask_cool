import datetime

from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")


    # user1 = User()
    # user1.name = "Jim"
    # user1.surname = "Green"
    #
    # user2 = User()
    # user2.name = "Matt"
    # user2.surname = "Meleh"
    #
    # user3 = User()
    # user3.name = "Milred"
    # user3.surname = "Montag"
    #
    # user4 = User()
    # user4.name = "Aleksandr"
    # user4.surname = "Privalov"
    #
    # job1 = Jobs()
    # job1.team_leader_id = 1
    # job1.job = "important job"
    # job1.work_size = 15
    # job1.collaborators = "2, 3"
    # job1.is_finished = True
    # job1.end_date = datetime.date(2024, 3, 1)
    # job1.start_date = datetime.date(2021, 4, 9)
    #
    # job2 = Jobs()
    # job2.team_leader_id = 4
    # job2.job = "not important job"
    # job2.work_size = 1
    # job2.collaborators = "1, 2"
    # job2.end_date = datetime.date(2025, 1, 1)
    # job2.start_date = datetime.date(2024, 5, 8)
    # job2.is_finished = False
    #
    # db_sess = db_session.create_session()
    # db_sess.add(user1)
    # db_sess.add(user2)
    # db_sess.add(user3)
    # db_sess.add(user4)
    #
    # db_sess.add(job1)
    # db_sess.add(job2)
    # db_sess.commit()





    # job1 = Jobs()
    # job1.team_leader = 1
    # job1.job = "очент важная работа с номером 1"
    # job1.work_size = 15
    # job1.is_finished = True
    # job1.collaborators = "2, 3"


    app.run()


# @app.route("/")
# def index():
#     db_sess = db_session.create_session()
#     news = db_sess.query(News).filter(News.is_private != True)
#     return render_template("index.html", news=news)


@app.route("/")
def work_plan():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    # team_leads = []
    # for i in news:
    #     team_leads.append(db_sess.query(User).filter(i.team_leader == User.id))
    # for i in range(len(team_leads)):
    #     team_leads[i] = f"{team_leads[i].surnamme}  {team_leads[i].name}"
    return render_template("index.html", jobs=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
