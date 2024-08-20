from flask import Blueprint, render_template, request
import podcast.adapters.repository as repo
import podcast.podcastbp.services as services


podcast_blueprint = Blueprint(
    'podcast_blueprint', __name__)


@podcast_blueprint.route('/podcast', methods=['GET'])
def description():
    podcast_id = int(request.args.get('id'))

    # podcast_about - podcast image, title, author, description
    p_about = services.podcast_about(podcast_id, repo.repo_instance)
    print(p_about)
    # categories the podcast falls under
    p_categories = services.podcast_categories(podcast_id, repo.repo_instance)
    print(p_categories)
    # episodes - list of episodes
    p_episodes = services.podcast_episodes(podcast_id, repo.repo_instance)
    print(p_episodes)

    # for episode_dict in p_episodes:
    #     truncated_description = ' '.join(episode_dict['episode_description'].split()[:20]) + '...' if len(
    #         episode_dict['episode_description'].split()) > 20 else episode_dict['episode_description']
    #
    #     formatted_output = f"""
    #     Episode Number: {episode_dict['episode_number']}
    #     Title: {episode_dict['episode_title']}
    #     Description: {truncated_description}
    #     Publish Date: {episode_dict['episode_date']}
    #     Length: {episode_dict['episode_length']}
    #     """
    #     print(formatted_output)

    return render_template(
        'description/description.html', p_about=p_about, p_episodes=p_episodes, p_categories=p_categories
    )