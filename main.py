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
    return render_template('home.html', title='ShareNews.com')

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


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host='127.0.0.1')
