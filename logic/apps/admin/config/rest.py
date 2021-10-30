from flask import Flask
from logic.libs.rest import rest

flask_app = None


def setup_rest(app: Flask) -> Flask:

    global flask_app

    flask_app = rest.config_flask_app(app)
    rest.load_routes_by_regex_path(app, 'logic/apps/*/routes')
