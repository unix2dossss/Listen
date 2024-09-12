from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.playlist.services as services


playlist_blueprint = Blueprint("playlist_bp", __name__)


@playlist_blueprint.route("/playlist", defaults={"facet_name": "podcasts"}, methods=["GET"])
@playlist_blueprint.route("/playlist/<facet_name>", methods=["GET"])
def playlist(facet_name):
    page = request.args.get("page", 1, type=int)
    per_page = 12
    max_pages_to_show = 5

    if facet_name == "podcasts":
        playlist_items = services.get_user_playlist_podcasts(repo.repo_instance)
        playlist_page_title = "Your Saved Podcasts"
    else:
        playlist_items = services.get_user_playlist_episodes(repo.repo_instance)
        playlist_page_title = "Your Saved Episodes"

    total_pages = (len(playlist_items) + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_page = max(1, page - max_pages_to_show // 2)
    end_page = min(total_pages, start_page + max_pages_to_show - 1)

    if end_page - start_page < max_pages_to_show:
        start_page = max(1, end_page - max_pages_to_show + 1)

    paginated_podcasts = playlist_items[(page - 1) * per_page : page * per_page]

    return render_template(
        "playlist/playlist.html",
        podcasts=paginated_podcasts,
        category_page_title=playlist_page_title,
        current_page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        facet_name=facet_name
    )
