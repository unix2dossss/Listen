from flask import Blueprint, render_template, request, redirect, url_for, session
import podcast.adapters.repository as repo
import podcast.playlist.services as services
import podcast.utilities.services as utilities

playlist_blueprint = Blueprint("playlist_bp", __name__)


@playlist_blueprint.route("/playlist", defaults={"facet_name": "podcasts"}, methods=["GET"])
@playlist_blueprint.route("/playlist/<facet_name>", methods=["GET"])
def playlist(facet_name):
    page = request.args.get("page", 1, type=int)
    max_pages_to_show = 5

    username = session["username"]
    user = utilities.get_user_by_username(username, repo.repo_instance)

    if facet_name == "podcasts":
        playlist_items = services.get_user_playlist_podcasts(user, repo.repo_instance)
        playlist_page_title = "Your Saved Podcasts"
        per_page = 12
    else:
        playlist_items = services.get_user_playlist_episodes(user, repo.repo_instance)
        playlist_page_title = "Your Saved Episodes"
        per_page = 3

    total_pages = (len(playlist_items) + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_page = max(1, page - max_pages_to_show // 2)
    end_page = min(total_pages, start_page + max_pages_to_show - 1)

    if end_page - start_page < max_pages_to_show:
        start_page = max(1, end_page - max_pages_to_show + 1)

    paginated_items = playlist_items[(page - 1) * per_page : page * per_page]

    return render_template(
        "playlist/playlist.html",
        paginated_items=paginated_items,
        category_page_title=playlist_page_title,
        current_page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        facet_name=facet_name
    )


@playlist_blueprint.route("/playlist/add/<item_type>/<item_id>/<podcast_id>/<page>", methods=["GET"])
def add_to_playlist(item_type, item_id, podcast_id, page):

    username = session["username"]
    user = utilities.get_user_by_username(username, repo.repo_instance)

    if item_type == 'podcast':
        services.add_to_podcast_playlist(user, podcast_id, repo.repo_instance)
    else:   # episode
        services.add_to_episode_playlist(user, item_id, repo.repo_instance)

    return redirect(url_for("podcast_blueprint.description", id=podcast_id, page=page))
