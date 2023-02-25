# flask-sqllacumy
from maypackage import db, login_manager
from datetime import datetime


from flask_login import UserMixin


# After Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# USER MODEL
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(60), default="dprof.png", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    notifications = db.Column(db.Integer, default=0, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # subjects = db.relationship('Subject', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}"


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    holder = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


# POST MODEL

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    mainImage = db.Column(db.String(20), nullable=True)
    type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post: '{self.title}'"


class SubImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
