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

# There is no point in fetching the data for the same place over and over again
# during the same day, because the output will be identical


@lru_cache(maxsize=500, typed=True)
def fetch_weather(today: datetime.date, lat: float, lon: float):
    return weather_api.fetch_weather(lat=lat, lon=lon)


def render_weather_table(weather_forecast: List) -> pd.DataFrame:
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


def register_callbacks(dash_app):
    @dash_app.callback(Output("main_page_lokalizacje_layer", "children"),
                       [Input("main_map", "click_lat_lng")])
    def map_click(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]

    # @dash_app.callback(Output('main_map_locc', 'children'),
    #                    [Input('main_map', 'click_lat_lng')])
    # def store_curr_location(click_lat_lng):
    #     if click_lat_lng is None:
    #         raise PreventUpdate
    #     click_lat_lng = [round(x, ndigits=2) for x in click_lat_lng]
    #     return click_lat_lng

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
