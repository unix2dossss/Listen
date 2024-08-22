from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.author.services as services
from flask import url_for, redirect

author_blueprint = Blueprint(
    'author_bp', __name__)


@author_blueprint.route('/author', methods=['GET'])
def all_authors():
    page = request.args.get('page', 1, type=int)  # Get the page number from the query parameters, default to 1
    per_page = 18  # Number of categories per page
    authors = services.get_all_authors(repo.repo_instance)

    # Calculate total pages
    total_pages = (len(authors) + per_page - 1) // per_page

    # Slice the categories list to get only the categories for the current page
    authors_paginated = authors[(page - 1) * per_page: page * per_page]

    return render_template(
        'all_authors.html',
        podcast_authors=authors_paginated,
        current_page=page,
        total_pages=total_pages
    )


@author_blueprint.route('/author/<author_name>', methods=['GET'])
def category_podcasts(author_name):
    url = url_for('discover_bp.podcasts_by_category', author_name=author_name)
    return redirect(url)
