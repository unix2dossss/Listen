from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.discover.services as services
from flask import url_for, redirect


discover_blueprint = Blueprint(
    'discover_bp', __name__)


@discover_blueprint.route('/discover', methods=['GET'])
def discover():
    # list of popular categories , editor picks, podcast-search list

    popular_categories = services.get_popular_categories(repo.repo_instance)

    editor_picks = services.get_editor_picks(repo.repo_instance)

    podcast_search_list = services.get_podcast_search_list(repo.repo_instance)

    return render_template(
        'discover/discover.html',
        popular_categories=popular_categories,
        editor_picks=editor_picks,
        podcast_search_list=podcast_search_list
    )


@discover_blueprint.route('/all_podcasts/<category_name>', methods=['GET'])
def podcasts_by_category(category_name):
    category_podcasts = None

    if category_name != 'all':
        category_podcasts = services.get_podcasts_in_category(category_name, repo.repo_instance)
        # print(category_podcasts)
    else:
        category_podcasts = services.get_all_podcasts(repo.repo_instance)

    return render_template(
        'all_podcasts.html',
        podcasts=category_podcasts[:12]
    )

@discover_blueprint.route('/editor_picks/<podcast_id>', methods=['GET'])
def editor_picked_podcast(podcast_id):
    # editor_picked_p = services.get_editor_picked_podcast(podcast_id, repo.repo_instance)
    url = url_for('podcast_blueprint.description', id=podcast_id)
    return redirect(url)

@discover_blueprint.route('/filtered_podcast/<podcast_id>', methods=['GET'])
def filtered_podcast(podcast_id):
    url = url_for('podcast_blueprint.description', id=podcast_id)
    return redirect(url)

