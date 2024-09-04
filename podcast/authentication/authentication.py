from flask import Blueprint, render_template, redirect, url_for, session, request
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from password_validator import PasswordValidator


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit"
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    username = StringField("Username",
                           [DataRequired(message="Your username is required")],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password",
                             [DataRequired(message="Your password is required"),
                              PasswordValid("Your password is invalid")], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Your username is required")], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Your password is required")], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")