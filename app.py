from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/dbtest')
def dbtest():
    room1 = models.Room(roomName="The Good Place")
    db.session.add(room1)
    db.session.commit()
    rooms = models.Room.query.all()

    return str(len(rooms)) + " - Hello"


if __name__ == '__main__':
    app.run()

