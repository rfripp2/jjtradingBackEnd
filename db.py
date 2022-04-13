from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app import app
import MySQLdb
import mysql.connector

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:juangv@localhost/test'
engine = create_engine('mysql+pymysql://root:juangv@localhost/test')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):

        return f"User('{self.username}')"


db.create_all()


user_1 = User(username='Juannn')
db.session.add(user_1)
db.session.commit()

User.query.first()
