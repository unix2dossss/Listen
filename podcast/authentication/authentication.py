from flask import Blueprint, render_template, redirect, url_for, session, request
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
import podcast.adapters.repository as repo
from podcast.authentication import services
from podcast.utilities import utilities
from functools import wraps

auth_blueprint = Blueprint("auth_bp", __name__, url_prefix='/auth')


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    from_register = request.args.get("from_register")
    from_logout = request.args.get("from_logout")

    print("TUNAKTUNAKTUNAKTUJNAK")
    print(from_register)
    print(from_logout)

    if request.referrer:
        if (
            from_register == 'true'
            or request.referrer.split("/")[-1] == "login?from_register=true"
        ):
            from_register = True
        else:
            from_register = False

    print("222222TUNAKTUNAKTUNAKTUJNAK")
    print(from_register)
    print(from_logout)

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
            session["logged_in"] = True

            return redirect(url_for("home_bp.home"))

        except services.AuthenticationException:
            try:
                services.get_user(username, repo.repo_instance)
                password_error = "The specified password does not match the username!"
            except services.UnknownUserException:
                username_error = "This username is not registered!"

    return render_template(
        "auth/login.html",
        username=utilities.get_username(),
        login_type="Login",
        form=form,
        username_error=username_error,
        password_error=password_error,
        login_modal=True,
        from_register=from_register,
        from_logout=from_logout,
    )


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    username_error = None
    password_error = None
    login_modal = False

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        services.add_user(username, password, repo.repo_instance)
        return redirect(url_for("auth_bp.login", from_register="true"))

    # Invalid Password
    if form.errors.get("password"):
        password_error = (
            "Your password must be at least 8 characters, "
            "and contain an upper case letter, lower case letter and a digit"
        )

    # Invalid Username
    if form.errors.get("username"):
        username_error = "This username is already taken!"
        login_modal = True

    return render_template(
        "auth/login.html",
        form=form,
        login_type="Register",
        password_error=password_error,
        username_error=username_error,
        login_modal=login_modal,
    )


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_bp.login", from_logout="true"))


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


class UsernameValid:
    def __init__(self, message=None):
        if not message:
            message = "This username is already taken!"
        self.message = message

    def __call__(self, form, field):
        try:
            services.username_exists(user_name=field.data, repo=repo.repo_instance)
        except services.UsernameExistsException:
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        [
            DataRequired(message="Your username is required"),
            UsernameValid("This username is already taken!"),
        ],
    )
    # username = StringField("Username",
    #                        [DataRequired(message="Your username is required")])
    password = PasswordField(
        "Password",
        [
            DataRequired(message="Your password is required"),
            PasswordValid("Your password is invalid"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", [DataRequired(message="Your username is required")]
    )
    password = PasswordField(
        "Password", [DataRequired(message="Your password is required")]
    )
    submit = SubmitField("Login")


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)
    return wrapped_view
