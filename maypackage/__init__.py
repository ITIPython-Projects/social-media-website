from flask import Flask, flash, render_template, url_for, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

# Login Imports
from flask_login import LoginManager

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = '/run/media/ahmedabdelrhman/New Volume/Courses______/ITI/Lectures/flask/labs/social media website/maypackage/static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)

from maypackage import routs
