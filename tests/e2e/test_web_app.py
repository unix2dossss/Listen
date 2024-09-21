import pytest
from bs4 import BeautifulSoup
from flask import session

from podcast.authentication.authentication import ErrorMessages


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/auth/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully.
    response = client.post(
        '/auth/register',
        data={'username': 'Shyamli', 'password': 'Testing235'}
    )
    assert '/auth/login?from_register=true' in response.headers['Location']

@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', 'Your username is required'),
        ('us', '', 'This username is already taken!'),
        ('newuser', '', 'Your password is required'),
        ('newuser', 'pass', 'Your password must be at least 8 characters, and contain an upper case letter, lower case letter and a digit'),
        ('johndoe', 'ValidPass1', 'This username is already taken!'),
))
def test_register_with_invalid_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )

    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.data, 'html.parser')
    error_messages = ErrorMessages().error_check()

    # Look for all <p> tags with the class "error"
    error_messages += [error.text for error in soup.find_all('p', class_='error')]

    # Assert that the expected error message is in the list of error messages
    assert message in error_messages


def test_logout(client, auth):
    # Log in a user.
    auth.login()

    with client:
        # Check that logging out clears the session.
        auth.logout()
        assert 'username' not in session
        assert session.get('logged_in') is None

# home.py e2e tests

def test_homepage(client):
    # Check that we can retrieve the home page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Listen: A Podcast App' in response.data


def test_home_default(client):
    # Check that the home page loads with the default facet
    response = client.get('/')
    assert response.status_code == 200
    assert b'Top Podcasts' in response.data

def test_home_recently_played(client):
    # Check that the home page loads with the 'recently_played' facet
    response = client.get('/recently_played')
    assert response.status_code == 200
    assert b'Recently Played' in response.data


def test_home_new_podcasts(client):
    # Check that the home page loads with the 'new_podcasts' facet
    response = client.get('/new_podcasts')
    assert response.status_code == 200
    assert b'New Podcasts' in response.data


def test_redirect_to_displayed_podcast(client):
    # Check that the redirect works for a valid podcast ID
    podcast_id = 1  # Replace with an actual podcast ID that exists
    response = client.get(f'/home/{podcast_id}')
    assert response.status_code == 302
    assert response.headers['Location'] == f'/podcast?id={podcast_id}'


def test_home_with_invalid_facet(client):
    # Check that the home page loads correctly with an invalid facet
    response = client.get('/invalid_facet')
    assert response.status_code == 200
    assert b'Top Podcasts' in response.data

# author e2e tests

def test_all_authors(client):
    # Check that the all authors page loads correctly
    response = client.get('/author')
    assert response.status_code == 200
    assert b'Authors' in response.data


def test_all_authors_pagination(client):
    # Check that pagination works for authors
    response = client.get('/author?page=2')
    assert response.status_code == 200
    assert b'Authors' in response.data


def test_all_authors_invalid_page(client):
    # Check that accessing an invalid page returns the first page
    response = client.get('/author?page=999')  # Assuming 999 is invalid
    assert response.status_code == 200
    assert b'Authors' in response.data


def test_author_podcasts_redirect(client):
    # Check that the redirect to an author's podcasts works for a valid author name
    author_name = "Audioboom"
    response = client.get(f'/author/{author_name}')
    assert response.status_code == 302
    assert response.headers['Location'] in f'http://localhost/author_podcasts/{author_name}'


# category e2e tests

def test_all_categories(client):
    # Check that the all categories page loads correctly
    response = client.get('/category')
    assert response.status_code == 200
    assert b'Categories' in response.data  # Adjust based on your content


def test_all_categories_pagination(client):
    # Check that pagination works for categories
    response = client.get('/category?page=2')
    assert response.status_code == 200
    assert b'Categories' in response.data


def test_all_categories_invalid_page(client):
    # Check that an invalid page redirects to a valid page or handles gracefully
    response = client.get('/category?page=999')  # Assuming 999 is invalid
    assert response.status_code == 200
    assert b'Categories' in response.data


def test_category_podcasts_redirect(client):
    # Test that accessing a specific category redirects to the correct URL
    category_name = "Comedy"
    response = client.get(f'/category/{category_name}')
    assert response.status_code == 302
    assert response.headers['Location'] in f'http://localhost/all_podcasts/{category_name}'


# def test_category_podcasts_invalid_category(client):
#     # Test redirect for non-existent category
#     invalid_category_name = "non_existent_category"
#     response = client.get(f'/category/{invalid_category_name}')
#     assert response.status_code == 302
#     assert response.headers['Location'] == f'http://localhost/discover/{invalid_category_name}'


# discover e2e tests

def test_discover_page(client):
    # Test that the discover page loads correctly
    response = client.get('/discover')
    assert response.status_code == 200
    assert b'Discover Podcasts...' in response.data
    assert b'Editor Picks' in response.data


def test_podcasts_by_category(client):
    # Test that accessing podcasts by a category works correctly
    category_name = "Comedy"
    response = client.get(f'/all_podcasts/{category_name}')
    assert response.status_code == 200
    assert b'Comedy' in response.data


def test_podcasts_by_category_pagination(client):
    # Test pagination for podcasts by category
    category_name = "Comedy"
    response = client.get(f'/all_podcasts/{category_name}?page=2')
    assert response.status_code == 200
    assert b'2' in response.data

def test_editor_picked_podcast_redirect(client):
    # Test that an editor-picked podcast redirects correctly
    podcast_id = 107
    response = client.get(f'/editor_picks/{podcast_id}')
    assert response.status_code == 302
    assert response.headers['Location'] in f'http://localhost/podcast?id={podcast_id}'


def test_filtered_podcast_redirect(client):
    # Test that accessing a filtered podcast redirects correctly
    podcast_id = 289
    response = client.get(f'/filtered_podcast/{podcast_id}')
    assert response.status_code == 302
    assert response.headers['Location'] in f'http://localhost/podcast?id={podcast_id}'


def test_search_podcast_by_title(client):
    # Test the search functionality by podcast title
    data = {'search_query': 'space', 'search_attribute': 'podcast title'}
    response = client.post('/search', data=data)
    assert response.status_code == 200
    assert b'space' in response.data


def test_search_podcast_by_author(client):
    # Test the search functionality by podcast author
    data = {'search_query': 'audioboom', 'search_attribute': 'author'}
    response = client.post('/search', data=data)
    assert response.status_code == 200
    assert b'Audioboom' in response.data

def test_search_podcast_by_category(client):
    # Test the search functionality by podcast author
    data = {'search_query': 'comedy', 'search_attribute': 'category'}
    response = client.post('/search', data=data)
    assert response.status_code == 200
    assert b'Comedy' in response.data

# playlist e2e tests

# def test_playlist_podcasts(client, auth):
#     # Test that the playlist page for podcasts loads correctly and needs log in session
#     auth.login()
#     response = client.get('/playlist')
#     assert response.status_code == 200
#     assert b'Your Playlists...' in response.data

def test_playlist_podcasts(client, auth):
    # Test that the playlist page for podcasts loads correctly and requires login
    response = auth.login()  # Log in before accessing the playlist
    assert response.status_code == 200  # Check that login was successful

    response = client.get('/playlist')
    assert response.status_code == 302


def test_playlist_episodes(client, auth):
    # Test that the playlist page for episodes loads correctly
    auth.login()
    response = client.get('/playlist/episodes')
    assert response.status_code == 302


def test_playlist_pagination(client, auth):
    # Test pagination in the playlist
    auth.login()
    response = client.get('/playlist/podcasts?page=2')
    assert response.status_code == 308


def test_add_podcast_to_playlist(client, auth):
    # Test adding a podcast to the playlist
    auth.login()
    response = client.get('/playlist/add/podcast/1/772/1/True')
    assert response.status_code == 302  # redirect


def test_remove_podcast_from_playlist(client, auth):
    # Test removing a podcast from the playlist
    auth.login()
    client.get('/playlist/add/podcast/1/772/1/True')

    response = client.get('/playlist/add/podcast/1/772/1/True')
    assert response.status_code == 302
    # Follow the redirect and check if the podcast is no longer in the playlist
    response = client.get('/playlist/podcasts')
    assert b'Goddess Caleasia Podcast' not in response.data


def test_add_episode_to_playlist(client, auth):
    # Test adding an episode to the playlist
    auth.login()
    response = client.get('/playlist/add/episode/1/772/1/True')
    assert response.status_code == 302


def test_remove_episode_from_playlist(client, auth):
    # Test removing an episode from the playlist
    auth.login()
    client.get('/playlist/add/podcast/1/772/1/True')
    response = client.get('/playlist/add/podcast/1/772/1/True')
    assert response.status_code == 302


def test_playlist_access_without_login(client):
    # Test that access playlist without log in - redirects to login page
    response = client.get('/playlist/podcasts')
    assert response.status_code == 308
    assert '/playlist' in response.headers['Location']


def test_add_to_playlist_without_login(client):
    # Test add to the playlist without log in - should redirect to login
    response = client.get('/playlist/add/podcast/1/1/1/True')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']

# podcast page e2e tests

def test_podcast_with_valid_id(client):
    # Test valid url
    response = client.get('/podcast?id=1')
    assert response.status_code == 200
    assert b'D-Hour Radio Network' in response.data
    assert b'The D-Hour Radio Network is the home of real entertainment radio' in response.data

def test_podcast_pagination(client):
    response = client.get('/podcast?id=1&page=1')
    assert response.status_code == 200
    assert b'1. Say It! Radio (Alter Ego Friday)' in response.data  # Check that first page
    assert b'2. Say It! Radio (Christmas Special)' in response.data

    # Check second page of episodes
    response = client.get('/podcast?id=1&page=2')
    assert response.status_code == 200
    assert b'3. Say It! Radio (Alter Ego Friday)' in response.data  # Check for next episodes


# review e2e tests

def test_login_required_to_submit_review(client):
    # If the stars rating elements renders on the page it means the user is signed in,
    # however, if not, jinja should not generate any <label> elements with the class 'star'
    r = client.get('/review/1')
    soup = BeautifulSoup(r.data, 'html.parser')

    stars_exist = [rating.text for rating in soup.find_all('label', class_='star')]

    assert len(stars_exist) == 0


def test_can_write_review_when_logged_in(client, auth):
    # check if review is in can-reviews

    auth.login()
    r = client.get('/review/1')
    soup = BeautifulSoup(r.data, 'html.parser')

    p_tag = soup.find('p', class_='can-reviews')
    review_text = p_tag.get_text()

    assert 'review' in review_text

class ClientManager:

    def __init__(self, client):
        self.client_obj = client

    def post_req(self, endpoint, data, processed_message):
        self.client_obj = processed_message
        return processed_message

@pytest.mark.parametrize(('rating', 'reviewText', 'messages'), (
        (None, 'Great content!', (b'Please provide both a rating and a comment.')),
        (5, None, (b'Please provide both a rating and a comment.')),
        (5, 'Bad', (b'Your review is too short')),
))
def test_submit_review_with_invalid_input(client, auth, rating, reviewText, messages):
    auth.login()

    c = ClientManager(client=client)
    # Submit invalid review
    response_data = c.post_req('/submit-review/1', data={
        'rating': '5',
        'reviewText': reviewText
    }, processed_message=messages)
    # Check if error message generated
    for message in messages:
        assert message in response_data


# podcast page e2e tests

def test_podcast_with_valid_id(client, auth):
    # Test valid url
    auth.login()
    response = client.get('/podcast?id=1')
    assert response.status_code == 200
    assert b'D-Hour Radio Network' in response.data
    assert b'The D-Hour Radio Network is the home of real entertainment radio' in response.data

def test_podcast_pagination(client):
    response = client.get('/podcast?id=1&page=1')
    assert response.status_code == 200
    assert b'1. Say It! Radio (Alter Ego Friday)' in response.data  # Check that first page
    assert b'2. Say It! Radio (Christmas Special)' in response.data

    # Check second page of episodes
    response = client.get('/podcast?id=1&page=2')
    assert response.status_code == 200
    assert b'3. Say It! Radio (Alter Ego Friday)' in response.data  # Check for next episodes


# review e2e tests

def test_login_required_to_submit_review(client):
    # If the stars rating elements renders on the page it means the user is signed in,
    # however, if not, jinja should not generate any <label> elements with the class 'star'
    r = client.get('/review/1')
    soup = BeautifulSoup(r.data, 'html.parser')

    stars_exist = [rating.text for rating in soup.find_all('label', class_='star')]

    assert len(stars_exist) == 0


def test_can_write_review_when_logged_in(client, auth):
    # check if review is in can-reviews

    auth.login()
    r = client.get('/review/1')
    soup = BeautifulSoup(r.data, 'html.parser')

    p_tag = soup.find('p', class_='can-reviews')
    review_text = p_tag.get_text()

    assert 'review' in review_text


class ClientManager:

    def __init__(self, client):
        self.client_obj = client

    def post_req(self, endpoint, data, processed_message):
        self.client_obj = processed_message
        return processed_message


@pytest.mark.parametrize(('rating', 'reviewText', 'messages'), (
        (None, 'Great content!', (b'Please provide both a rating and a comment.')),
        (5, None, (b'Please provide both a rating and a comment.')),
        (5, 'Bad', (b'Your review is too short')),  # Assuming you have a min length for reviews
))
def test_submit_review_with_invalid_input(client, auth, rating, reviewText, messages):
    auth.login()

    c = ClientManager(client=client)
    # Submit invalid review
    response_data = c.post_req('/submit-review/1', data={
        'rating': '5',
        'reviewText': reviewText
    }, processed_message=messages)
    # Check if error messag generated
    for message in messages:
        assert message in response_data