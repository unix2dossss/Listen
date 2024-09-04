from flask import Blueprint, render_template, redirect, url_for, session, request
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
import podcast.adapters.repository as repo
from podcast.authentication import services
from podcast.utilities import utilities

auth_blueprint = Blueprint("auth_bp", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # utilities.check_valid_session(repo.repo_instance)

    form = LoginForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data

            services.authenticate_user(username, password, repo.repo_instance)

            session.clear()
            session["username"] = username

            return redirect(url_for("home_bp.home"))

        except services.AuthenticationException:
            try:
                services.get_user(username, repo.repo_instance)
                password_error = "The specified password does not match the username!"
            except services.UnknownUserException:
                username_error = "This username is not registered!"

    # utilities.check_valid_session(repo.repo_instance)

    return render_template(
        "auth/login.html",
        username=utilities.get_username(),
        login_type="Login",
        form=form,
        username_error=username_error,
        password_error=password_error,
        login_modal=True
    )


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    password_error = None  # Initialize password_error as None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        services.add_user(username, password, repo.repo_instance)
        return redirect(url_for("auth_bp.login"))

    # If form validation fails, check if it's the password causing the issue
    if form.errors.get("password"):
        password_error = ("Your password must be at least 8 characters, "
                          "and contain an upper case letter, lower case letter and a digit")

    return render_template(
        "auth/login.html",
        form=form,
        login_type="Register",
        password_error=password_error,
        login_modal=False
    )


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
                           [DataRequired(message="Your username is required")])
    password = PasswordField("Password",
                             [DataRequired(message="Your password is required"),
                              PasswordValid("Your password is invalid")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Your username is required")])
    password = PasswordField("Password", [DataRequired(message="Your password is required")])
    submit = SubmitField("Login")
