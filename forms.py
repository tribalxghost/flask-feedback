from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,EmailField
from wtforms.validators import InputRequired,Length


class RegisterForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(max=20)])
    password = PasswordField('Password', [InputRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    first_name = StringField('First Name', [InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', [InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(max=20)])
    password = PasswordField('Password', [InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title', [InputRequired(), Length(max=100)])
    content = StringField('Content', [InputRequired()])
    