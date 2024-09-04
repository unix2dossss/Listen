from podcast.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from podcast.adapters.repository import AbstractRepository


def add_user(user_name: str, password: str, repo: AbstractRepository):
    password_hash = generate_password_hash(password)
    user = User(1, user_name, password_hash)
    repo.add_user(user)