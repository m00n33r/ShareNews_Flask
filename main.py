from flask import Flask, render_template, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.__all_models import User, News
from forms import RegisterForm, LoginForm, AddNew, UserBio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/logs.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/home')
def home():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    return render_template('home.html', title='ShareNews.com', news=news)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.email.data) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(form.name.data) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(form.password.data) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif form.password.data != form.password_again.data:
            flash('Passwords don\'t match.', category='error')

        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data):
            flash('This user is already exists', category='error')

        user = User(name=form.name.data,
                    age=form.age.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/features')
def features():
    return render_template('features.html', title='Features')


@app.route('/new/<int:new_id>')
def new(new_id):
    db_sess = db_session.create_session()
    new = db_sess.query(News).filter(News.id == new_id).first()
    user = db_sess.query(User).filter(new.user_id == User.id).first()
    return render_template('new.html', title=new.title,
                           new=new, user=user)


@app.route('/bio', methods=['POST', 'GET'])
def bio():
    session = db_session.create_session()
    news = session.query(News).filter(current_user.id == News.user_id).all()
    user = session.query(User).filter(current_user.id == User.id).first()

    msg = ''
    form = UserBio()
    if form.validate_on_submit():
        arr = []
        if form.name.data:
            arr.append('имя')
            user.name = form.name.data
        if form.email.data:
            arr.append('почту')
            user.email = form.email.data
        if form.password.data == form.password_again.data and form.password.data:
            arr.append('пароль')
            user.set_password(form.password.data)
        if form.bio.data:
            arr.append('информацию о себе')
            user.bio = form.bio.data
        msg += 'Вы успешно сменили ' + ', '.join(arr) + '.'
        session.commit()
    return render_template('bio.html', form=form, title='Личный кабинет', news=news, message=msg)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    form = AddNew()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('newpost.html', title='Добавить новость',
                                   form=form, message='Вы не вошли в систему')
        db_sess = db_session.create_session()
        added_new = News(title=form.title.data,
                         content=form.content.data,
                         is_private=form.private.data,
                         user_id=current_user.id)
        db_sess.add(added_new)
        db_sess.commit()
        return redirect('/home')
    return render_template('newpost.html', title='Добавить новость', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host='127.0.0.1')
