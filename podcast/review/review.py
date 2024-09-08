from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, request, flash
import podcast.adapters.repository as repo
import podcast.review.services as services
import podcast.podcastbp.services as podcastbp_services
import podcast.utilities.utilities as utilities
from podcast.domainmodel.model import Review, Comment

review_blueprint = Blueprint("review_bp", __name__)


# Route to display and handle the review form
@review_blueprint.route("/submit-review/<podcast_id>", methods=["POST"])
def submit_review(podcast_id):
    podcast_id = int(podcast_id)
    rating = int(request.form.get("rating"))
    review_text = request.form.get("reviewText")

    print(rating)
    print(review_text)

    if not rating or not review_text:
        flash("Please provide both a rating and a comment.", "error")
        return redirect(url_for("review_bp.review", podcast_id=podcast_id))

    username = utilities.get_username()
    current_user = utilities.get_user_by_username(username, repo.repo_instance)
    print(username)
    print(current_user)

    # Don't allow if the user has already reviewed a podcast
    if services.user_has_reviewed_podcast(current_user, podcast_id, repo.repo_instance):
        flash("You have already reviewed this podcast.", "error")
        print("you have already reviewed this podcast")
        return redirect(url_for("review_bp.review", podcast_id=podcast_id))

    # Create a comment
    now = datetime.now()
    new_comment = Comment(current_user, review_text, now)
    # Create a review
    new_review = Review(current_user, new_comment, rating)
    services.add_review(new_review, podcast_id, repo.repo_instance)

    flash("Your review has been submitted!", "success")
    return redirect(url_for("review_bp.review", podcast_id=podcast_id))


# Route to display the review page
@review_blueprint.route("/review/<podcast_id>", methods=["GET"])
def review(podcast_id):
    podcast_id = int(podcast_id)
    # Get podcast details to display on the page
    p_about = podcastbp_services.podcast_about(podcast_id, repo.repo_instance)
    p_categories = podcastbp_services.podcast_categories(podcast_id, repo.repo_instance)
    p_reviews = services.get_reviews_of_podcast(podcast_id, repo.repo_instance)
    p_reviews_dict = services.podcast_reviews_dict(p_reviews)
    print(p_reviews_dict)

    username = utilities.get_username()
    current_user = utilities.get_user_by_username(username, repo.repo_instance)
    print(username)
    print(current_user)

    # Disable Submit Button if user has already reviewed!
    submit_disabled = services.user_has_reviewed_podcast(
        current_user, podcast_id, repo.repo_instance
    )
    print(submit_disabled)

    return render_template(
        "review/review.html",
        p_about=p_about,
        p_categories=p_categories,
        p_reviews=p_reviews_dict,
        submit_disabled=submit_disabled,
    )


# Redirect to the podcast page after reviewing
@review_blueprint.route("/review/episode/redirect/<podcast_id>", methods=["GET"])
def redirect_to_podcast(podcast_id):
    return redirect(url_for("podcast_blueprint.description", id=podcast_id))
