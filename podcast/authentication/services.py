from podcast.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from podcast.adapters.repository import AbstractRepository


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    password_hash = generate_password_hash(password)
    user = User(1, user_name, password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if not user:
        raise UnknownUserException
    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)

    if user is not None:
        print("OKAY USER EXISTS")
        authenticated = check_password_hash(user.password, password)

    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    user_dict = {"user_name": user.username, "password": user.password}
    return user_dict
