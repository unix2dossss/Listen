from flask import Blueprint, render_template, url_for, redirect
import podcast.adapters.repository as repo
import podcast.podcastbp.services as services


review_blueprint = Blueprint(
    'review_bp', __name__)


@review_blueprint.route('/review/<podcast_id>', methods=['GET'])
def review(podcast_id):
    podcast_id = int(podcast_id)
    # podcast_about - podcast image, title, author, description
    p_about = services.podcast_about(podcast_id, repo.repo_instance)
    # categories the podcast falls under
    p_categories = services.podcast_categories(podcast_id, repo.repo_instance)

    return render_template(
        'review/review.html',
        p_about=p_about,
        p_categories=p_categories
    )


@review_blueprint.route('/review/episode/redirect/<podcast_id>', methods=['GET'])
def redirect_to_podcast(podcast_id):
    url = url_for('podcast_blueprint.description', id=podcast_id)
    return redirect(url)
