import dash_table

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_leaflet as dl

from typing import List

from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_leaflet.express as dlx

from datetime import datetime
from functools import lru_cache

from dashboard.features.weather_api_featching import WeatherAPI

def fetch_profile_data():
    moje_dane = {
            'id'        : 1,
            'Imie'     : 'TestImie',
            'Nazwisko'      : 'TestNazwisko',
            'Email': 'test@email.com'
        }
    return moje_dane


def register_callbacks(dash_app):
    @dash_app.callback([Output("profile-first-name", "value"),
                        Output("profile-last-name", "value"),
                        Output("profile-email", "value")],
                       [Input('url', 'pathname')])
    def show_profile_info(url):
        if url != '/profil-szczegoly':
            raise PreventUpdate

        profile = fetch_profile_data()

        return profile['Imie'], profile['Nazwisko'], profile['Email']
