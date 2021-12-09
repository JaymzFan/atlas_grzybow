import dash
from flask import Flask

import dash_bootstrap_components as dbc

from config import Config


def create_app():
    server = Flask(__name__)
    server.config.from_object(Config)
    register_dashapps(server)
    register_extensions(server)

    return server


def register_dashapps(app):
    from dashboard.content import layout
    from dashboard.callbacks.Navigation import register_callbacks
    from dashboard.callbacks.InteractiveMaps import register_callbacks as rc_maps
    from dashboard.callbacks.ManagingFriends import register_callbacks as rc_friends

    dashapp = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/',
                        external_stylesheets=[dbc.themes.BOOTSTRAP],
                        suppress_callback_exceptions=True)

    with app.app_context():
        dashapp.title = Config.APP_TITLE
        dashapp.layout = layout
        register_callbacks(dashapp)
        rc_maps(dashapp)
        rc_friends(dashapp)

def register_extensions(server):
    from dashboard.extensions import db
    from dashboard.extensions import login

    db.init_app(server)
    login.init_app(server)
