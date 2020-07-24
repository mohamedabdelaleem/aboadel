from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, default=' ')
    added_at = db.Column(db.DateTime, default=datetime.now())
    videos = db.relationship('Video', backref='section')


class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    i_frame = db.Column(db.String, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.now())
    section_id = db.Column(db.Integer,db.ForeignKey('section.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Video : %r>' % self.title

if __name__ == '__main__':
    manager.run()
