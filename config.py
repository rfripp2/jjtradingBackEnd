from flask_sqlalchemy import SQLAlchemy
import redis
from dotenv import load_dotenv
import os

load_dotenv()


class ApplicationConfig:
    SECRET_KEY = "qyvKmPkXF2wbSgCdv72qr2ccdCSXJiHZ"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
