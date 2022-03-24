import datetime

from flask import Flask, render_template, redirect,  request, make_response, session, abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.news import News
from forms.register import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.loginform import LoginForm
from forms.add_news import AddNews
from forms.add_job import AddJobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route("/all_jobs")
def work_plan():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("jobs.html", jobs=jobs)


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
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/news")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/add_news", methods=["GET", "POST"])
@login_required
def add_news():
    form = AddNews()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            about_it=form.about_it.data,
            is_private=form.is_private.data,
            user_id=current_user.id
        )
        db_conn = db_session.create_session()
        db_conn.add(news)
        db_conn.commit()
        redirect("/news")
    else:
        return render_template("add_news.html", form=form, title="Add News")


@app.route("/news")
def news():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("news.html", news=news)


@app.route('/add_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = AddNews()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.about_it.data = news.about_it
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.about_it = form.about_it.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('add_news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news')


@app.route("/add_jobs", methods=["GET", "POST"])
@login_required
def add_jobs():
    form = AddJobs()
    if form.validate_on_submit():
        name = form.team_leader_name.data
        surname = form.team_leader_surname.data
        db_conn = db_session.create_session()
        id_lead = db_conn.query(User).filter(User.name == name, User.surname == surname).all()
        start = form.start_date.data.split("-")
        start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        end = form.finish_date.data.split("-")
        end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=start_date,
            end_date=end_date,
            is_finished=form.is_finished.data,
            team_leader_id=id_lead[0].id
        )
        db_conn.add(job)
        db_conn.commit()
        return redirect("all_jobs")
    else:
        return render_template("add_job.html", form=form, title="Add Job")


@app.route("/add_jobs/<int:id>", methods=["GET", "POST"])
@login_required
def change_job(id):
    form = AddJobs()
    db_sess = db_session.create_session()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            team_lead = jobs.team_leader

            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.finish_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
            form.team_leader_name.data = team_lead.name
            form.team_leader_surname.data = team_lead.surname
        else:
            abort(404)

    elif form.validate_on_submit():
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            data_start_str = str(form.start_date.data).split("-")
            data_start = datetime.date(int(data_start_str[0]), int(data_start_str[1]), int(data_start_str[2]))

            data_end_str = str(form.finish_date.data).split("-")
            data_end = datetime.date(int(data_end_str[0]), int(data_end_str[1]), int(data_end_str[2]))

            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = data_start
            jobs.end_date = data_end
            jobs.is_finished = form.is_finished.data
            new_team_lid = db_sess.query(User).filter(User.name == form.team_leader_name.data,
                                                      User.surname == form.team_leader_surname.data).first()

            jobs.team_leader_id = new_team_lid.id
            db_sess.commit()
            return redirect('/all_jobs')
        else:
            abort(404)
    return render_template("add_job.html", form=form, title="Change Job")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/all_jobs')


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/news")


if __name__ == '__main__':
    main()
