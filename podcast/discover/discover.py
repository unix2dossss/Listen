from flask import Blueprint, render_template


discover_blueprint = Blueprint(
    'discover_bp', __name__)


@discover_blueprint.route('/discover', methods=['GET'])
def discover():
    return render_template(
        'discover/discover.html'
    )