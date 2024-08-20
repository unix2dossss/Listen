from flask import Blueprint, render_template, url_for, redirect
import podcast.adapters.repository as repo
import podcast.home.services as services


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html'
    )



    # if category_name != 'all':
    #     category_podcasts = services.get_podcasts_in_category(category_name, repo.repo_instance)
    #     # print(category_podcasts)
    # else:
    #     category_podcasts = services.get_all_podcasts(repo.repo_instance)
    #     category_page_title = "All Podcasts..."
    #
    # return render_template(
    #     'all_podcasts.html',
    #     podcasts=category_podcasts[:12], category_page_title=category_page_title
    # )

@home_blueprint.route('/<facet_name>', methods=['GET'])
def podcasts_by_facet(facet_name):
    display_podcasts = services.get_top_podcasts(repo.repo_instance)

    if facet_name == 'recently_played':
        display_podcasts = services.get_recently_played(repo.repo_instance)
    elif facet_name == 'new_podcasts':
        display_podcasts = services.get_new_podcasts(repo.repo_instance)

    return render_template(
        'home/home.html',
        podcasts=display_podcasts
    )
