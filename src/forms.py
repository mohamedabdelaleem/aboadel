from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError



class Log_in_form(FlaskForm):
    email = StringField('Email', validators=[Email(message='^This field must be Email.'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    