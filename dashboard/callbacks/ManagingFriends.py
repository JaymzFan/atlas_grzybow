from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate

from dashboard.models import Friends, Users
from dashboard.extensions import db


import json


def register_callbacks(dash_app):
    @dash_app.callback(Output("lista-znajomych", "children"),
                       [Input('url', 'pathname')],
                       [State('znajomi-storage', 'data'),
                        State('logged_in_username', 'data')])
    def wyswietl_liste_znajomych(url, data, un):
        if url != '/profil-znajomi':
            raise PreventUpdate
        un = un['un']

        friendships = Friends.query.filter_by(friend1=un).all()
        friendships = [x.friend2 for x in friendships]
        friendships = list(set(friendships))
        return str(friendships)

    @dash_app.callback(Output("add_friend_status", "children"),
                       [Input('add_friend-submit', 'n_clicks')],
                       [State('add_friend_name', 'value')])
    def dodaj_znajomego(n_clicks, username):
        if n_clicks == 0:
            raise PreventUpdate

        if username is None:
            return ""

        user_found = Users.query.filter_by(username=username).first()
        if user_found:
            friendship = Friends(friend1='adam', friend2=username)
            db.session.add(friendship)
            db.session.commit()
            return f'Dodano {username} do list'
        return f'Nie można znaleźć użytkownika {username}'

    @dash_app.callback(Output("remove_friend_status", "children"),
                       [Input('remove_friend-submit', 'n_clicks')],
                       [State('remove_friend_name', 'value'),
                        State('logged_in_username', 'data')])
    def usun_znajomego(n_clicks, username, current_un):
        if n_clicks == 0:
            raise PreventUpdate

        current_un = current_un['un']

        friendship = Friends.query.filter_by(friend1=current_un, friend2=username).all()
        for friend in friendship:
            db.session.delete(friend)
        db.session.commit()

        if username is None:
            return ""

        return f'Usunieto znajomość z {username}'
