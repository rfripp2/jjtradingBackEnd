from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class User(db.Model):

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.String)
    reports = db.relationship("ReportMinsMax", backref="owner")


class ReportMinsMax(db.Model):

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    coins_requested = db.Column(db.Integer)
    days_back = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    max = db.Column(db.Integer)
    min = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Integer)
