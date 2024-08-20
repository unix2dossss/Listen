from flask import Blueprint, render_template, url_for, redirect
import podcast.adapters.repository as repo
import podcast.home.services as services


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', defaults={'facet_name': 'top_podcasts'}, methods=['GET'])
@home_blueprint.route('/<facet_name>', methods=['GET'])
def home(facet_name):

    if facet_name == 'recently_played':
        display_podcasts = services.get_recently_played(repo.repo_instance)
    elif facet_name == 'new_podcasts':
        display_podcasts = services.get_new_podcasts(repo.repo_instance)
    else:
        display_podcasts = services.get_top_podcasts(repo.repo_instance)

    continue_listening_list = services.get_continue_listening_podcasts(repo.repo_instance)
    top_authors = services.get_top_authors(repo.repo_instance)

    return render_template(
        'home/home.html',
        facet_podcasts=display_podcasts,
        continue_listening=continue_listening_list,
        top_authors=top_authors,
        facet_name=facet_name
    )


@home_blueprint.route('/home/<podcast_id>', methods=['GET'])
def get_displayed_podcast(podcast_id):
    url = url_for('podcast_blueprint.description', id=podcast_id)
    return redirect(url)


