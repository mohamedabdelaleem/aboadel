from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)



class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    i_frame = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
