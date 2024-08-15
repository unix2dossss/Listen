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
    print(p_about.keys())
    # categories the podcast falls under
    p_categories = services.podcast_categories(podcast_id, repo.repo_instance)
    print(p_categories)
    # episodes - list of episodes

    return render_template(
        'description/description.html',
    )
