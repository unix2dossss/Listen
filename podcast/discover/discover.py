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
    category_id = request.args.get('category_id')

    if category_id is not None:
        print("hello" + category_id)
        podcasts = services.get_podcasts_by_category(int(category_id), repo.repo_instance)
        print(podcasts)

    return render_template(
        'all_podcasts.html'
    )
