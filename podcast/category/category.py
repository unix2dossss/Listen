from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.category.services as services
from flask import url_for, redirect

category_blueprint = Blueprint("category_bp", __name__)


@category_blueprint.route("/category", methods=["GET"])
def all_categories():
    page = request.args.get(
        "page", 1, type=int
    )  # Get the page number from the query parameters, default to 1
    per_page = 18  # Number of categories per page
    categories = services.get_all_categories(repo.repo_instance)

    # Calculate total pages
    total_pages = (len(categories) + per_page - 1) // per_page

    # Slice the categories list to get only the categories for the current page
    categories_paginated = categories[(page - 1) * per_page : page * per_page]

    return render_template(
        "all_categories.html",
        podcast_categories=categories_paginated,
        current_page=page,
        total_pages=total_pages,
    )


@category_blueprint.route("/category/<category_name>", methods=["GET"])
def category_podcasts(category_name):
    url = url_for("discover_bp.podcasts_by_category", category_name=category_name)
    return redirect(url)
