# import flask
from maypackage import *
from werkzeug.utils import secure_filename
from maypackage.forms import RegistrationForm, LoginForm, PostForm, SubjectForm
from maypackage.model import *
from flask import request
import os
# hashing password
from flask_bcrypt import Bcrypt
# Login Manger
from flask_login import login_user, current_user, logout_user, login_required

bcrypt = Bcrypt()


# login imports


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = PostForm()
        posts = Post.query.filter_by(type='public')
        not_friends = (
            db.session.query(User)
            .outerjoin(
                Friends,
                db.and_(
                    current_user.id == Friends.receiver,
                    User.id == Friends.sender,
                )
            )
            .outerjoin(
                Requests,
                db.and_(
                    current_user.id == Requests.sender,
                    User.id == Requests.holder,
                )
            )
            .filter(Friends.id == None)
            .filter(Requests.id == None)
            .filter(User.id != current_user.id)
            .all()
        )
        if form.validate_on_submit():
            with app.app_context():
                mainimage = request.files['mainimage']
                if mainimage.filename:
                    imagename = secure_filename(mainimage.filename)
                    post = Post(user_id=current_user.id, title=form.title.data, content=form.content.data,
                                mainImage=imagename, type=request.form.get('type'))
                    db.session.add(post)
                    db.session.commit()
                    mainimage.save(os.path.join(app.config['UPLOAD_FOLDER'], "post", imagename))
                else:
                    post = Post(user_id=current_user.id, title=form.title.data, content=form.content.data,
                                type=request.form.get('type'))
                    db.session.add(post)
                    db.session.commit()
                db.session.flush()
                subimages = request.files.getlist('images')
                for subimg in subimages:
                    imagename = secure_filename(subimg.filename)
                    subimgObj = SubImages(image=imagename, user_id=post.id)
                    db.session.add(subimgObj)
                    db.session.commit()
                    subimg.save(os.path.join(app.config['UPLOAD_FOLDER'], "post", imagename))
        return render_template('index.html', form=form, posts=posts, not_friends=not_friends)
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


@app.route('/addfriend/<user_id>')
def add_friend(user_id):
    with app.app_context():
        req = Requests(holder=user_id, sender=current_user.id)
        db.session.add(req)

        notfiy = Notifications(user_id=current_user.id,
                               description=f"{current_user.username} Send You a Friends Request")
        db.session.add(notfiy)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        friends = Friends.query.filter_by(receiver=current_user.id)
        return render_template('profile.html', friends=friends)
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
