from flask import Blueprint, session
import podcast.utilities.services as services
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


utilities_blueprint = Blueprint("utilities_bp", __name__)


def get_n_podcasts(quantity=3):
    podcasts = services.get_n_podcasts(quantity)
    return podcasts


def get_username():
    username = None
    if "username" in session:
        username = session["username"]
    return username


def get_user_by_username(username: str, repo: AbstractRepository):
    return services.get_user_by_username(username, repo)
