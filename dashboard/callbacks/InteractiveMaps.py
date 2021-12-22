import dash_bootstrap_components as dbc
import dash_html_components as html

from datetime import datetime

from functools import lru_cache

from dash.dependencies import Input, Output, State

import dash_leaflet as dl

from dash.exceptions import PreventUpdate

from dashboard.features.weather_api_featching import WeatherAPI

import dash_table

import pandas as pd

from typing import List


weather_api = WeatherAPI(API_KEY='0e62530620448044eb4a76de6180486e')


@lru_cache(maxsize=500, typed=True)
def fetch_weather(today: datetime.date, lat: float, lon: float):
    return weather_api.fetch_weather(lat=lat, lon=lon)


def render_weather_table(weather_forecast: List) -> pd.DataFrame:
    print(weather_forecast)
    df = pd.DataFrame.from_records(weather_forecast)
    df = df.transpose()
    df.reset_index()
    df['Dane'] = df.index
    df = df[['Dane', 0, 1, 2, 3, 4, 5, 6, 7]]
    df.columns = df.loc['dzien']
    df.rename(columns={'dzien': 'Dane'})
    df = df.drop('dzien')
    dt = dash_table.DataTable(
            id='weather_forecast_dt',
            columns=[{'name': i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_as_list_view=True,
            style_cell={
                'font_size': '0.2rem'
            }
    )
    return dt


def from_datestr_to_wday_polish(datestr: str) -> str:
    eng_wday = datetime.strptime(datestr, '%Y-%m-%d').strftime('%A')
    pol_wdays = {
        "Monday": "Poniedziałek",
        "Tuesday": "Wtorek",
        "Wednesday": "Środa",
        "Thursday": "Czwartek",
        "Friday": "Piątek",
        "Saturday": "Sobota",
        "Sunday": "Niedziela"
    }
    return pol_wdays[eng_wday]


def render_weather_tables(weather_forecast: List) -> List:

    forcasts_cards = []
    for x in weather_forecast:
        weather_card = dbc.Card(
                dbc.CardBody([
                    html.H2(from_datestr_to_wday_polish(datestr=x['dzien'])),
                    html.P(x['dzien'], className="lead"),
                    html.P(x['pogoda'].capitalize()),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(dbc.Label('Wschód słońca'), width=4),
                        dbc.Col(x['wschod_slonca'], width=8)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Temp. rano (℃)'), width=4),
                        dbc.Col(x['temperatura_poranek'], width=8)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Temp. południe (℃)'), width=4),
                        dbc.Col(x['temperatura_poludnie'], width=8)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Wilgotność'), width=4),
                        dbc.Col(x['wilgotnosc'], width=8)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Zachmurzenie'), width=4),
                        dbc.Col(x['zachmurzenie'], width=8)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Prawd. opadów'), width=4),
                        dbc.Col(x['prawdop_opadow'], width=8)
                    ], className="mb-3")
                ])
        )
        forcasts_cards.append(dbc.Col(weather_card, width=12))

    return forcasts_cards


def register_callbacks(dash_app):
    @dash_app.callback(Output("main_page_lokalizacje_layer", "children"),
                       [Input("main_map", "click_lat_lng")])
    def map_click(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]

    @dash_app.callback(Output('prognoza_pogody', 'children'),
                       [Input('main_map', 'click_lat_lng')])
    def get_weather_forecast(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        click_lat_lng = [round(x, ndigits=1) for x in click_lat_lng]
        today_date = datetime.now().date()

        pogoda_teraz = fetch_weather(today=today_date,
                                     lat=click_lat_lng[0],
                                     lon=click_lat_lng[1])
        return render_weather_table(weather_forecast=pogoda_teraz)

    @dash_app.callback(Output('weather_forecast_placeholder', 'children'),
                       [Input('main_map', 'click_lat_lng')])
    def get_weather_forecast2(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        click_lat_lng = [round(x, ndigits=1) for x in click_lat_lng]
        today_date = datetime.now().date()

        pogoda_teraz = fetch_weather(today=today_date,
                                     lat=click_lat_lng[0],
                                     lon=click_lat_lng[1])

        return render_weather_tables(weather_forecast=pogoda_teraz)


