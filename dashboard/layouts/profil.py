import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import json

szczegoly = html.Div([
    html.H1("Profil szczegoly"),
    html.Div(id='current_user_welcome')
])

znajomi = dbc.Container([
    dcc.Store(id='znajomi-storage', data=json.dumps({'friends_list': ['user1', 'user2']})),

    dbc.Row(dbc.Col(html.H1("Znajomi"), width='auto')),
    dbc.Row(dbc.Col(html.Div(id='lista-znajomych'))),
    dbc.Row(dbc.Col(html.H3('Dodaj znajomego do listy'))),
    dbc.Row([
        dbc.Col(dbc.Input(id='add_friend_name', placeholder='username')),
        dbc.Col(dbc.Button('Dodaj', id='add_friend-submit'))
    ]),
    dbc.Row(dbc.Col(html.Div(id='add_friend_status'))),
    dbc.Row(dbc.Col(html.H3('Usuń znajomego z listy'))),
    dbc.Row([
        dbc.Col(dbc.Input(id='remove_friend_name', placeholder='username')),
        dbc.Col(dbc.Button('Usuń', id='remove_friend-submit'))
    ]),
    dbc.Row(dbc.Col(html.Div(id='remove_friend_status')))
])

zaloguj = html.Div([
    html.H1("Profil zaloguj")
])

