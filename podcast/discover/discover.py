from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.discover.services as services


discover_blueprint = Blueprint(
    'discover_bp', __name__)


@discover_blueprint.route('/discover', methods=['GET'])
def discover():
    # list of popular categories , editor picks, podcast-search list

    return render_template(
        'discover/discover.html'
    )


@discover_blueprint.route('/all_podcasts/<category_name>', methods=['GET'])
def podcasts_by_category(category_name):
    category_podcasts = None

    if category_name != 'All':
        category_podcasts = services.get_podcasts_in_category(category_name, repo.repo_instance)
        # print(category_podcasts)

    return render_template(
        'all_podcasts.html',
        podcasts=category_podcasts[:12]
    )

@discover_blueprint.route('/all_podcasts/all', methods=['GET'])
def searched_podcasts():
    searched_podcast_list = services.get_all_podcasts(repo.repo_instance)

    return render_template(
        'all_podcasts.html',
        podcasts=searched_podcast_list[:12]
    )


