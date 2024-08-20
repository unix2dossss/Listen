from flask import Blueprint, render_template, url_for, redirect
import podcast.adapters.repository as repo
import podcast.home.services as services


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    # url = url_for('home_bp.podcasts_by_facet', facet_name="top_podcasts")
    # return redirect(url)
    display_podcasts = services.get_top_podcasts(repo.repo_instance)
    continue_listening_list = services.get_continue_listening_podcasts(repo.repo_instance)
    top_authors = services.get_top_authors(repo.repo_instance)

    return render_template(
        'home/home.html',
        facet_podcasts=display_podcasts,
        continue_listening=continue_listening_list,
        top_authors=top_authors,
    )


@home_blueprint.route('/<facet_name>', methods=['GET'])
def podcasts_by_facet(facet_name):
    display_podcasts = services.get_top_podcasts(repo.repo_instance)
    continue_listening_list = services.get_continue_listening_podcasts(repo.repo_instance)
    top_authors=services.get_top_authors(repo.repo_instance)

    if facet_name == 'recently_played':
        display_podcasts = services.get_recently_played(repo.repo_instance)
    elif facet_name == 'new_podcasts':
        display_podcasts = services.get_new_podcasts(repo.repo_instance)

    return render_template(
        'home/home.html',
        facet_podcasts=display_podcasts,
        continue_listening=continue_listening_list,
        top_authors=top_authors,
        facet_name=facet_name
    )
