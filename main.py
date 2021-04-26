from flask import Flask
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/logs.db")


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host='127.0.0.1')
