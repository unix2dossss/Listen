from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review
from datetime import datetime


def podcast_reviews_dict(reviews: list[Review]):
    formatted_dict = []
    for i in range(len(reviews)):
        review_dict = dict()
        review_dict["initial"] = reviews[i].owner.username[0].upper()
        review_dict["reviewer"] = reviews[i].owner.username.title()
        review_date = reviews[
            i
        ].comment.comment_date  # Assuming this is a datetime object
        review_dict["datetime"] = review_date.strftime("%d %B %Y &bull; %I:%M %p")
        review_dict["comment"] = reviews[i].comment_text
        review_dict["rating_full"] = reviews[i].rating
        review_dict["rating_empty"] = 5 - reviews[i].rating
        formatted_dict.append(review_dict)
    return formatted_dict


def get_reviews_of_podcast(podcast_id, repo: AbstractRepository):
    return repo.get_reviews_of_podcast(podcast_id)


def user_has_reviewed_podcast(current_user, podcast_id, repo: AbstractRepository):
    print("current user id:", current_user.id)
    reviews = get_reviews_of_podcast(podcast_id, repo)
    for review in reviews:
        print(review)
        if review.owner == current_user:
            print("review user id:", review.owner.id)
            return True
    return False


def add_review(review, podcast_id, repo: AbstractRepository):
    repo.add_review(review, podcast_id)
