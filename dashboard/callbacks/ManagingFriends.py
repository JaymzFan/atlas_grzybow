import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate

from dashboard.models import Friends, Users
from dashboard.extensions import db

from typing import List


from database.DatabaseInterface import DatabaseSessionManager, DatabaseFacade

from config import get_db_uri

from sqlalchemy import create_engine



def fetch_my_friends(user_id):
    # Prepare connection to Database
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    return db.fetch_friends_ids(user_id=user_id)


def fetch_all_usernames():
    # Prepare connection to Database
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )
    all_users = db.users.fetch_all_users()
    all_users = [x.__dict__["username"] for x in all_users]
    return all_users


def render_friends_list(friends: List[str]) -> List:
    return [dbc.ListGroupItem(x) for x in friends]


def register_callbacks(dash_app):
    @dash_app.callback(
        Output("lista-znajomych", "children"),
        [Input("url", "pathname")],
        State("logged_in_username", "data"),
    )
    def wyswietl_liste_znajomych(url, un):
        if url != "/profil-znajomi":
            raise PreventUpdate

        friends_list = fetch_my_friends(user_id=un["un"])
        friends_list = sorted(list(set([x["username"] for x in friends_list])))
        return render_friends_list(friends_list)

    @dash_app.callback(
        Output("dropdown_friends_to_add", "options"),
        [Input("url", "pathname")],
        State("logged_in_username", "data"),
    )
    def wyswietl_liste_znajomych_do_dodania(url, un):
        if url != "/profil-znajomi":
            raise PreventUpdate

        options_list = fetch_all_usernames()
        friends_list = fetch_my_friends(user_id=un["un"])
        friends_list = sorted(list(set([x["username"] for x in friends_list])))
        options_list = [
            {"label": x, "value": x}
            for x in options_list
            if x != un["un"] and x not in friends_list
        ]
        return options_list

    @dash_app.callback(
        Output("dropdown_friends_to_remove", "options"),
        [Input("url", "pathname")],
        State("logged_in_username", "data"),
    )
    def wyswietl_liste_znajomych_do_usuniecia(url, un):
        if url != "/profil-znajomi":
            raise PreventUpdate

        friends_list = fetch_my_friends(user_id=un["un"])
        friends_list = sorted(list(set([x["username"] for x in friends_list])))
        friends_list = [{"label": x, "value": x} for x in friends_list]
        return friends_list

    @dash_app.callback(
        Output("alert-added-friend", "is_open"),
        [Input("add_friend-submit", "n_clicks")],
        [
            State("dropdown_friends_to_add", "value"),
            State("logged_in_username", "data"),
        ],
    )
    def dodaj_znajomego(n_clicks, username, current_user):
        if n_clicks == 0:
            raise PreventUpdate

        if username is None:
            return False

        current_user = current_user["un"]
        all_users_friends = [
            x["username"] for x in fetch_my_friends(user_id=current_user)
        ]

        if current_user == username:
            return False
        if username in all_users_friends:
            return False

        user_found = Users.query.filter_by(username=username).first()
        if user_found:
            friendship = Friends(friend1=current_user, friend2=username)
            db.session.add(friendship)
            db.session.commit()

            return True
        return False

    @dash_app.callback(
        Output("alert-removed-friend", "is_open"),
        [Input("remove_friend-submit", "n_clicks")],
        [
            State("dropdown_friends_to_remove", "value"),
            State("logged_in_username", "data"),
        ],
    )
    def usun_znajomego(n_clicks, username, current_un):
        if n_clicks == 0:
            raise PreventUpdate

        current_un = current_un["un"]

        friendship = Friends.query.filter_by(friend1=current_un, friend2=username).all()
        for friend in friendship:
            db.session.delete(friend)
        db.session.commit()

        if username is None:
            return False

        return True
