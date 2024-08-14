from flask import Blueprint, request, render_template, redirect, url_for, session

import podcast.adapters.repository as repo
import podcast.utilities.services as services

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


# description page related methods
def get_podcast_episodes():
    pass


# discover page related methods
def get_popular_categories(quantity):
    # returns a list of categories for the discover page
    pass


def get_editor_picks(quantity):
    # returns a list of podcasts for the discover page
    pass


def get_podcast_by_filter(filter_condition):
    # search bar filter in discover page
    pass


# homepage related methods
def get_recently_played(quantity):
    pass


def get_new_podcasts(quantity):
    pass


def get_recently_listening(quantity):
    pass


def get_top_authors(quantity):
    pass
