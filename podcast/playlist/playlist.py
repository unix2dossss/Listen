from flask import Blueprint, render_template, url_for, redirect
import podcast.adapters.repository as repo
import podcast.playlist.services as services


playlist_blueprint = Blueprint("playlist_bp", __name__)


@playlist_blueprint.route("/playlist", defaults={"facet_name": "top_podcasts"}, methods=["GET"])
@playlist_blueprint.route("/playlist/<facet_name>", methods=["GET"])
def home(facet_name):
    return render_template(
        "playlist/playlist.html",
    )