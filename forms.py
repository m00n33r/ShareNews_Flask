from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Никнейм', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddNew(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = StringField('Содержание', validators=[DataRequired()])
    private = BooleanField('Приватно')
    submit = SubmitField('Добавить')


class UserBio(FlaskForm):
    name = StringField('Сменить имя')
    email = EmailField('Сменить почту')
    password = PasswordField('Сменить пароль')
    password_again = PasswordField('Повторите новый пароль')
    bio = StringField('Обо мне')
    submit = SubmitField('Сохранить')
