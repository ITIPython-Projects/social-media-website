# flask-sqllacumy
from maypackage import db, login_manager
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy import or_

from flask_login import UserMixin


# After Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# USER MODEL
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(60), default="dprof.png", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    notifications = db.Column(db.Integer, default=0, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def friends_number(self):
        return Friends.query.filter_by(receiver=self.id).count()

    def get_friends(self):
        friends = db.session.query(User).join(
            Friends,
            db.and_(self.id == Friends.receiver,
                    User.id == Friends.sender,
                    )
        )
        return friends
    # friends = Friends.query.filter(or_(Friends.sender.like(self.id),
    #                                    Friends.receiver.like(self.id)))
    # friends_ids = []
    # for friend in friends:
    #     if self.id == friend.sender:
    #         friends_ids.append(friend.receiver)
    #     else:
    #         friends_ids.append(friend.sender)
    # return User.query.filter(User.id.in_(friends_ids)).all()


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
    subImages = db.relationship('SubImages', backref='author', lazy=True)
    user = db.relationship("User", backref=backref("user", uselist=False))

    def __repr__(self):
        return f"Post: '{self.title}'"


class SubImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"{self.image}"
