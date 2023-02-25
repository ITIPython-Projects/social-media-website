# import flask
from maypackage import *
from werkzeug.utils import secure_filename
from maypackage.forms import RegistrationForm, LoginForm, SubjectForm
from maypackage.model import User, Post
from flask import request
import os
# hashing password
from flask_bcrypt import Bcrypt
# Login Manger
from flask_login import login_user, current_user, logout_user, login_required

bcrypt = Bcrypt()


# login imports


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Save User
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            image = request.files['image']
            if image.filename:
                imagename = secure_filename(image.filename)
                user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                            image=imagename)
                db.session.add(user)
                db.session.commit()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], "user", imagename))

            else:
                user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                            image="dprof.png")
                db.session.add(user)
                db.session.commit()

        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', form=form, error=1)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# -------------- POSTS ------------------------

@app.route('/subjects', methods=['GET', 'POST'])
def subject_Add():
    form = SubjectForm()
    if form.title.data:
        users = request.form.get('users')
        for userId in users:
            with app.app_context():
                subjectobj = Subject(title=form.title.data, details=form.details.data, user_id=userId)
                db.session.add(subjectobj)
                db.session.commit()
        user = User.query.filter_by(id=userId).first()
        print(user.subjects)
    usersobj = User.query.all()
    return render_template('subjectAdd.html', form=form, usersobj=usersobj, title="subject_Add Form")
