from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .model import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'UserName',
        validators=[
                    DataRequired()
                    , Length(min=2, max=20)
                   ]
                 )
    email = StringField(
        'Email',
        validators=[
                    DataRequired(),
                    Length(min=2, max=100),
                    Email()
                   ]
                 )
    password = PasswordField(
        'passowrd',
        validators=[
                    DataRequired(),
                   ]
                 )
    confirmPassword = PasswordField(
        'Confirm Password',
        validators=[
                    DataRequired(),
                    EqualTo('password')
                   ]
                 )
    submit = SubmitField(
        'Sign Up',
                 )

    # custom validation for duplicates
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    username = StringField(
        'UserName',
        validators=[
                    DataRequired()
                    , Length(min=2, max=20)
                   ]
                 )
    password = PasswordField(
        'passowrd',
        validators=[
                    DataRequired(),
                   ]
                 )
    submit = SubmitField(
        'Submit',
                 )
class SubjectForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
                    DataRequired()
                    , Length(min=2, max=20)
                   ]
                 )
    details = StringField(
        'Details',
        validators=[
                    DataRequired(),
                   ]
                 )
    title = StringField(
        'Title',
        validators=[
                    DataRequired()
                    , Length(min=2, max=20)
                   ]
                 )
    submit = SubmitField(
        'Submit',
                 )

