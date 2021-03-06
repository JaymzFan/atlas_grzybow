import dash
from flask import Flask

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
    from dashboard.callbacks.manage_locations import register_callbacks as rc_addnew_loc
    from dashboard.callbacks.ManagingFriends import register_callbacks as rc_friends
    from dashboard.callbacks.MushroomsPage import register_callbacks as rc_mushrooms
    from dashboard.callbacks.ProfileManagement import register_callbacks as rc_profile

    dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname="/",
        external_stylesheets=["/assets/bootstrap.min.css"],
        suppress_callback_exceptions=True
    )

    with app.app_context():
        dashapp.title = Config.APP_TITLE
        dashapp.layout = layout
        register_callbacks(dashapp)
        rc_maps(dashapp)
        rc_friends(dashapp)
        rc_mushrooms(dashapp)
        rc_addnew_loc(dashapp)
        rc_profile(dashapp)


def register_extensions(server):
    from dashboard.extensions import db
    from dashboard.extensions import login

    db.init_app(server)
    login.init_app(server)
