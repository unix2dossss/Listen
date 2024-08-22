from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.author.services as services
from flask import url_for, redirect

author_blueprint = Blueprint(
    'author_bp', __name__)


@author_blueprint.route('/author', methods=['GET'])
def all_authors():
    page = request.args.get('page', 1, type=int)
    per_page = 18
    max_pages_to_show = 5

    author_podcasts = services.get_all_authors(repo.repo_instance)

    total_pages = (len(author_podcasts) + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_page = max(1, page - max_pages_to_show // 2)
    end_page = min(total_pages, start_page + max_pages_to_show - 1)

    if end_page - start_page < max_pages_to_show:
        start_page = max(1, end_page - max_pages_to_show + 1)

    paginated_authors = author_podcasts[(page - 1) * per_page: page * per_page]

    return render_template(
        'all_authors.html',
        podcast_authors=paginated_authors,
        current_page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
    )


@author_blueprint.route('/author/<author_name>', methods=['GET'])
def author_podcasts(author_name):
    url = url_for('discover_bp.podcasts_by_author', author_name=author_name)
    return redirect(url)
