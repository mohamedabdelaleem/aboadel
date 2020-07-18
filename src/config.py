import os

DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
