from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.podcastbp.services as services


podcast_blueprint = Blueprint(
    'podcast_blueprint', __name__)


@podcast_blueprint.route('/podcast', methods=['GET'])
def description():
    podcast_id = int(request.args.get('id'))

    # podcast_about - podcast image, title, author, description
    p_about = services.podcast_about(podcast_id, repo.repo_instance)
    # categories the podcast falls under
    p_categories = services.podcast_categories(podcast_id, repo.repo_instance)
    # episodes - list of episodes
    p_episodes = services.podcast_episodes(podcast_id, repo.repo_instance)

    return render_template(
        'description/description.html', p_about=p_about, p_episodes=p_episodes, p_categories=p_categories
    )
