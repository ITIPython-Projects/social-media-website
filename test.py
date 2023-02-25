from maypackage import db, app
from maypackage.model import User, Post
import sys


# create DB
def create_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
