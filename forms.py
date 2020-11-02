from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField , PasswordField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class PostForm(FlaskForm):
    item_name = StringField("Name of New Post", validators=[DataRequired()])
    description = TextAreaField("Text Field", validators=[DataRequired()],widget=TextArea())
    submit_button = SubmitField("Submit Post")
