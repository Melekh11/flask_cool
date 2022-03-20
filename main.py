from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    per = User()
    per.surname = "Scott"
    per.name = "Ridley"
    per.age = 21
    per.position = "captain"
    per.speciality = "research engineer"
    per.address = "module_1"
    per.email = "scott_chief@mars.org"

    per1 = User()
    per1.surname = "Matt"
    per1.name = "Meleh"
    per1.age = 16
    per1.position = "student"
    per1.speciality = "jun programmer"
    per1.address = "module_-1"
    per1.email = "cktkutxd@gmail.com"

    per2 = User()
    per2.surname = "Ann"
    per2.name = "Voronkova"
    per2.position = "teacher"
    per2.address = "module_your_free_time"
    per2.email = "not_your_business@gmail.com"

    db_sess = db_session.create_session()
    db_sess.add(per)
    db_sess.add(per1)
    db_sess.add(per2)
    db_sess.commit()

    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


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
