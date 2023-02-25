from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
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
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Email()
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField(
        'Sign Up',
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Email()
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField(
        'Log In',
    )


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
            , Length(min=5, max=20)
        ]
    )
    content = StringField(
        'Details',
        validators=[
            DataRequired(),
            Length(min=5)
        ]
    )

    submit = SubmitField(
        'Create',
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
