import dash_bootstrap_components as dbc

from sqlalchemy import create_engine

from dash import no_update

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

from dashboard.models import Users
from dashboard.extensions import db

from dashboard.layouts import header as nav_header
from dashboard.layouts import main_page
from dashboard.layouts import lokalizacje as nav_lokalizacje
from dashboard.layouts import grzyby as nav_grzyby
from dashboard.layouts import profil as nav_profil
from dashboard.layouts import logowanie as nav_logowanie

from config import get_db_uri

engine = create_engine(get_db_uri())

import json

def register_callbacks(dashapp):

    # ROUTING LOGOWANIA ------------------------------------------------------------
    @dashapp.callback(Output('url-rejestracja', 'pathname'),
                      [Input('submit-val', 'n_clicks')],
                      [State('username', 'value'),
                       State('password', 'value'),
                       State('useremail', 'value')])
    def rejestracja_usera(n_clicks, un, pw, em):
        if un is not None and pw is not None and em is not None:
            hashed_pass = generate_password_hash(pw, method='sha256')
            user = Users(username=un, password=hashed_pass, email=em)
            db.session.add(user)
            db.session.commit()

            return "/profil-logowanie"

        raise PreventUpdate

    # Logowanie
    @dashapp.callback([Output('url_login', 'pathname'),
                       Output('output-state', 'children'),
                       Output('logged_in_username', 'data')],
                      [Input('login-button', 'n_clicks')],
                      [State('uname-box', 'value'),
                       State('pwd-box', 'value')])
    def pwd_check(n_clicks, un, pwd):
        if un is None or pwd is None:
            raise PreventUpdate
        user = Users.query.filter_by(username=un).first()
        print(f"Logowanie: {un}")
        if user:
            if check_password_hash(user.password, pwd):
                login_user(user)
                return "/lokalizacje-przegladaj#", no_update, {"un": un}

        return no_update, dbc.Alert('Niewłaściwe hasło lub nazwa użytkownika', color='danger'), None

    # Przywitanie w panelu uzytkowniku
    @dashapp.callback(Output('current_user_welcome', 'children'),
                      Input('url', 'pathname'),
                      [State('logged_in_username', 'data')])
    def welcome_user(url, data):
        return f"Witaj {str(data['un'])}!"

    # ROUTING headera --------------------------------------------------------------
    @dashapp.callback(Output('header-content', 'children'),
                      Input('url', 'pathname'))
    def ustaw_header(url):
        if url == '/profil-wyloguj':
            return nav_header.navbar_niezalogowany

        if current_user.is_authenticated:
            return nav_header.navbar_zalogowany

        return nav_header.navbar_niezalogowany

    @dashapp.callback(Output('page-content', 'children'),
                      Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == "/index":
            return main_page.main_page
        elif pathname == '/profil-logowanie':
            return nav_logowanie.login
        elif pathname == '/profil-rejestracja':
            return nav_logowanie.create_account

        if not current_user.is_authenticated:
            return main_page.main_page
        elif pathname == '/profil-wyloguj':
            logout_user()
            return main_page.main_page
        elif pathname == '/lokalizacje-przegladaj':
            return nav_lokalizacje.main_page
        elif pathname == '/lokalizacje-modyfikuj':
            return nav_lokalizacje.manage
        elif pathname == '/grzyby-przegladaj':
            return nav_grzyby.main_page
        elif pathname == '/profil-szczegoly':
            return nav_profil.szczegoly
        elif pathname == '/profil-znajomi':
            return nav_profil.znajomi
        elif pathname == '/profil-rejestracja':
            return nav_logowanie.create_account
        elif pathname == '/profil-logowanie':
            return nav_logowanie.login

        return main_page.main_page