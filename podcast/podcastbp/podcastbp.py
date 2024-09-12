from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.podcastbp.services as services


podcast_blueprint = Blueprint("podcast_blueprint", __name__)


@podcast_blueprint.route("/podcast", methods=["GET"])
def description():
    podcast_id = int(request.args.get("id"))
    page = request.args.get("page", 1, type=int)
    per_page = 2  # Number of episodes per page
    max_pages_to_show = 5

    # podcast_about - podcast image, title, author, description
    p_about = services.podcast_about(podcast_id, repo.repo_instance)
    # categories the podcast falls under
    p_categories = services.podcast_categories(podcast_id, repo.repo_instance)
    # episodes - list of episodes
    p_episodes = services.podcast_episodes(podcast_id, repo.repo_instance)
    # average_rating of a podcast
    p_average_rating = services.get_podcast_average_rating(podcast_id, repo.repo_instance)
    # number of reviews podcast has
    p_review_count = services.get_podcast_review_count(podcast_id, repo.repo_instance)

    # Calculate pagination details
    total_episodes = len(p_episodes)
    total_pages = (total_episodes + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_page = max(1, page - max_pages_to_show // 2)
    end_page = min(total_pages, start_page + max_pages_to_show - 1)

    if end_page - start_page < max_pages_to_show:
        start_page = max(1, end_page - max_pages_to_show + 1)

    paginated_episodes = p_episodes[(page - 1) * per_page : page * per_page]

    return render_template(
        "description/description.html",
        p_about=p_about,
        p_episodes=paginated_episodes,
        p_categories=p_categories,
        current_page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        p_average_rating=p_average_rating,
        p_review_count=p_review_count
    )
