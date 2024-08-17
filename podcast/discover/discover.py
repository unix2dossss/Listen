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

@discover_blueprint.route('/podcasts_by_category', methods=['GET'])
def podcasts_by_category():
    category_name = request.args.get('category_name')

    category_podcasts = None

    if category_name is not None:
        print("hello" + category_name)
        category_podcasts = services.get_podcasts_in_category(category_name, repo.repo_instance)
        print(category_podcasts)

    else:
        category_podcasts = services.get_all_podcasts()

    return render_template(
        'all_podcasts.html',
        category_podcasts=category_podcasts
    )
