from database.db import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(128))
    new_path = db.Column(db.String(128))
    new_format = db.Column(db.String(10))
    status = db.Column(db.String(20))
    time_stamp = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tasks = db.relationship('Task', cascade='all, delete, delete-orphan')
