from datetime import datetime

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login, app
from config import Config

app_name = Config.app_name
current_year = Config.current_year


def is_admin():
    if current_user.role == 'admin':
        return True
    return False


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(), default='user')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.context_processor
def inject_variables():
    return dict(app_name=app_name, current_year=current_year)
