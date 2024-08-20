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
    page = request.args.get('page', 1, type=int)  # Get the page number from the query parameters, default to 1
    per_page = 12  # Number of podcasts per page
    max_pages_to_show = 5  # Max number of pages to show in pagination

    category_page_title = category_name

    if category_name == 'all':
        category_podcasts = services.get_all_podcasts(repo.repo_instance)
        category_page_title = "All Podcasts..."
    elif category_name == 'top_podcasts':
        category_podcasts = services.get_top_podcasts(repo.repo_instance)
        category_page_title = "Top Podcasts..."
    elif category_name == 'recently_played':
        category_podcasts = services.get_recently_played(repo.repo_instance)
        category_page_title = "Recently Played..."
    elif category_name == 'new_podcasts':
        category_podcasts = services.get_new_podcasts(repo.repo_instance)
        category_page_title = "New Podcasts..."
    else:
        category_podcasts = services.get_podcasts_in_category(category_name, repo.repo_instance)

    # Calculate total pages
    total_pages = (len(category_podcasts) + per_page - 1) // per_page

    # Ensure the current page is within the valid range
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # Calculate start and end page numbers for the pagination
    start_page = max(1, page - max_pages_to_show // 2)
    end_page = min(total_pages, start_page + max_pages_to_show - 1)

    # Adjust start page if we're near the end of the total pages
    if end_page - start_page < max_pages_to_show:
        start_page = max(1, end_page - max_pages_to_show + 1)

    paginated_podcasts = category_podcasts[(page - 1) * per_page: page * per_page]

    return render_template(
        'all_podcasts.html',
        podcasts=paginated_podcasts,
        category_page_title=category_page_title,
        current_page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        category_name=category_name
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
