from maypackage import db, app
from maypackage.model import *
import sys


# create DB
def create_db():
    with app.app_context():
        db.create_all()


def read_users():
    with app.app_context():
        print(User.query.all())


def make_frind():
    with app.app_context():
        friend = Friends(sender=5, receiver=2)
        db.session.add(friend)
        db.session.commit()


def make_request():
    with app.app_context():
        req = Requests(holder=6, sender=2)
        db.session.add(req)
        db.session.commit()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
