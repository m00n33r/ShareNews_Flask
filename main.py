from flask import Flask, render_template
from data import db_session
from data.__all_models import User, News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/logs.db")

@app.route('/')
@app.route('/home')
def home():
    session = db_session.create_session()
    return render_template('home.html', title='ShareNews.com')


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host='127.0.0.1')
