from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.category.services as services
from flask import url_for, redirect

category_blueprint = Blueprint(
    'category_bp', __name__)


@category_blueprint.route('/category', methods=['GET'])
def all_categories():
    categories = services.get_all_categories(repo.repo_instance)

    return render_template(
        'all_categories.html', podcast_categories=categories[:24]
    )

@category_blueprint.route('/category/<category_name>', methods=['GET'])
def category_podcasts(category_name):
    url = url_for('discover_bp.podcasts_by_category', category_name=category_name)
    return redirect(url)

