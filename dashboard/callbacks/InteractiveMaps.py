import dash_table

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_leaflet as dl

from typing import List

from dash import callback_context, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_leaflet.express as dlx

from datetime import datetime
from datetime import date

from functools import lru_cache

from dashboard.features.weather_api_featching import WeatherAPI

from database.DatabaseInterface import DatabaseSessionManager, DatabaseFacade

from config import get_db_uri

from sqlalchemy import create_engine


weather_api = WeatherAPI(API_KEY='0e62530620448044eb4a76de6180486e')


@lru_cache(maxsize=500, typed=True)
def fetch_weather(today: datetime.date, lat: float, lon: float):
    return weather_api.fetch_weather(lat=lat, lon=lon)


def fetch_locations_data(owner_id):
    # Prepare connection to Database
    db = DatabaseFacade(session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri())))

    data = db.fetch_locations_data(owner_id=owner_id,
                                   shared_with_user_id=owner_id)

    return data


@lru_cache(maxsize=3, typed=True)
def fetch_mushrooms_availability(today_month: str):
    # Prepare connection to Database
    db = DatabaseFacade(session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri())))

    dataset = {}
    for x in db.fetch_mushrooms_data():
        dataset[x['MushroomNameInFormal']] = x['MonthsAvailable'][today_month]
    return dataset


# # TODO: pamiętaj o deduplikacji. Ta sama lokalizacja moze byc udostepniona i byc moja
# def fetch_locations_data():
#     demo_data = [
#         {
#             'id'        : 1,
#             'location'  : {'lng': 21, 'lat': 51, 'radius_in_meters': 2500},
#             'Nazwa'     : 'Lokalizacja 1',
#             'Opis'      : 'Opis 1',
#             'Grzyby'    : ['Grzyb2', 'Grzyb3', "Grzyb6"],
#             'Shared_by' : None,
#             'Shared_with': [{'id': 1, 'username': 'user1'}],
#             'prywatnosc': "public"
#         },
#         {
#             'id'        : 2,
#             'location'  : {'lng': 21, 'lat': 52, 'radius_in_meters': 500},
#             'Nazwa'     : 'Lokalizacja 2',
#             'Opis'      : 'Opis 2',
#             'Grzyby'    : ['Grzyb1', 'Grzyb3'],
#             'Shared_by' : None,
#             'Shared_with':  [{'id': 2, 'username': 'user2'}],
#             'prywatnosc': "public"
#         },
#         {
#             'id'        : 3,
#             'location'  : {'lng': 21, 'lat': 53, 'radius_in_meters': 150},
#             'Nazwa'     : 'Lokalizacja 3',
#             'Opis'      : 'Opis 3',
#             'Grzyby'    : ['Grzyb1', 'Grzyb3'],
#             'Shared_by' : 'Mietek',
#             'Shared_with':  [{'id': 1, 'username': 'user1'},
#                              {'id': 2, 'username': 'user2'}],
#             'prywatnosc': "shared_with_me"
#         },
#         {
#             'id'        : 4,
#             'location'  : {'lng': 21, 'lat': 54, 'radius_in_meters': 350},
#             'Nazwa'     : 'Lokalizacja 4',
#             'Opis'      : 'Opis 4',
#             'Grzyby'    : ['Grzyb1'],
#             'Shared_by' : None,
#             'Shared_with': [],
#             'prywatnosc': "my_location"
#         }
#     ]
#     return demo_data


# def fetch_mushrooms_availability():
#     demo_data = {
#         'Grzyb1': False,
#         'Grzyb2': True,
#         'Grzyb3': False,
#         'Grzyb4': True,
#         'Grzyb5': True,
#         'Grzyb6': True,
#         'Grzyb7': True,
#         'Grzyb8': True
#     }
#     return demo_data


def render_geojson(data):
    data = [
        dict(lat=x['location']['lat'], lon=x['location']['lng'], popup=x['Nazwa'], id_lokalizacji=x['id'])
        for x in data]

    return data


def get_mushrooms_types():
    db = DatabaseFacade(session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri())))

    typy_grzybow = []
    for x in db.fetch_mushrooms_data():
        typy_grzybow.append(x['MushroomNameInFormal'])
    return typy_grzybow


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
                        dbc.Col(dbc.Label('Wschód słońca'), width=8),
                        dbc.Col(x['wschod_slonca'], width=4)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Temp. rano (℃)'), width=8),
                        dbc.Col(x['temperatura_poranek'], width=4)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Temp. południe (℃)'), width=8),
                        dbc.Col(x['temperatura_poludnie'], width=4)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Wilgotność'), width=8),
                        dbc.Col(x['wilgotnosc'], width=4)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Zachmurzenie'), width=8),
                        dbc.Col(x['zachmurzenie'], width=4)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col(dbc.Label('Prawd. opadów'), width=8),
                        dbc.Col(x['prawdop_opadow'], width=4)
                    ], className="mb-3")
                ])
        )
        forcasts_cards.append(dbc.Col(weather_card, width=12))

    return forcasts_cards


def get_my_friends(user_id):
    db = DatabaseFacade(session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri())))

    my_friends = db.fetch_friends_ids(user_id=user_id)
    return [{'id': x['id'], 'username': x['username']} for x in my_friends]

    # return [
    #     {'id': 1, 'username': 'user1'},
    #     {'id': 2, 'username': 'user2'},
    #     {'id': 3, 'username': 'user3'},
    #     {'id': 4, 'username': 'user4'},
    #     {'id': 5, 'username': 'user5'},
    #     {'id': 6, 'username': 'user6'}
    # ]


def register_callbacks(dash_app):
    @dash_app.callback(Output("main_page_lokalizacje_layer", "children"),
                       [Input("main_map", "click_lat_lng")])
    def map_click(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]

    @dash_app.callback(Output('weather_forecast_placeholder', 'children'),
                       [Input('store-current-location-data', 'data')])
    def get_weather_forecast2(curr_data):
        if curr_data is None:
            raise PreventUpdate

        click_lat_lng = [round(x, ndigits=1) for x in [curr_data['location']['lat'],
                                                       curr_data['location']['lng']]]
        today_date = datetime.now().date()

        pogoda_teraz = fetch_weather(today=today_date,
                                     lat=click_lat_lng[0],
                                     lon=click_lat_lng[1])

        return render_weather_tables(weather_forecast=pogoda_teraz)

    @dash_app.callback(Output("locations_filters", "is_open"),
                       Input('locations_show_filters', 'n_clicks'),
                       State("locations_filters", "is_open"))
    def pokaz_filtry(n_clicks, is_open):
        if n_clicks:
            return not is_open

        return is_open

    @dash_app.callback([Output("locations_filters_loctypes", "value"),
                        Output('locations_filters_mushroomtypes', 'value')],
                       [Input('locations_clear_filters', 'n_clicks'),
                        Input('button-mark-sesonal-mushrooms', 'n_clicks')],
                       [State("locations_filters_loctypes", "options"),
                        State("locations_filters_mushroomtypes", "options")])
    def wyczysc_filtry(n_clicks,
                       n_clicks_seasonal_mushrooms,
                       location_types,
                       mushrooms_options):
        if n_clicks == 0:
            raise PreventUpdate
        if n_clicks_seasonal_mushrooms == 0:
            raise PreventUpdate

        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if trigger == 'button-mark-sesonal-mushrooms':
            seasonal_mushrooms_info = fetch_mushrooms_availability(today_month=str(date.today().month))
            seasonal_mushrooms = [x[0] for x in seasonal_mushrooms_info.items() if x[1] is True]
            all_mushrooms = [x['value'] for x in mushrooms_options if x['value'] in seasonal_mushrooms]
            return no_update, all_mushrooms

        all_values = [x['value'] for x in location_types]
        return list(set(all_values)), []

    @dash_app.callback(Output("store-all-locations-data", "data"),
                       Input('url', 'pathname'),
                       State('logged_in_username', 'data'))
    def load_locations_data(url, un):
        if url != '/lokalizacje-przegladaj':
            raise PreventUpdate

        return fetch_locations_data(owner_id=un['id'])

    @dash_app.callback(Output("store-filtered-locations-ids", "data"),
                       Input('locations_apply_filters', 'n_clicks'),
                       Input('locations_clear_filters', 'n_clicks'),
                       [State("locations_filters_loctypes", "value"),
                        State('locations_filters_mushroomtypes', 'value'),
                        State('store-all-locations-data', 'data')])
    def filter_locations(n_clicks, n_clics_clear, loc_types, mushroom_types, all_locations):
        if n_clicks == 0 or n_clics_clear == 0:
            raise PreventUpdate

        if all_locations is None:
            raise PreventUpdate

        # filter by location type
        filt_loc = [x for x in all_locations
                    if x['prywatnosc'] in loc_types]

        # filter by mushrooms
        # all locations in which at least one mushroom from the list is available
        if mushroom_types:
            filt_loc = [
                x for x in filt_loc if any(y in mushroom_types for y in x['Grzyby'])
            ]

        return filt_loc

    @dash_app.callback(Output("locations_filters_mushroomtypes", "options"),
                       Input('store-all-locations-data', 'data'))
    def filter_mushrooms(all_locations):
        if all_locations is None:
            raise PreventUpdate

        return [{'label': x, 'value': x} for x in get_mushrooms_types()]

    @dash_app.callback(Output("locations_filtered_number", "children"),
                       Input("store-filtered-locations-ids", "data"),
                       Input("locations_clear_filters", "n_clicks"),
                       State('store-all-locations-data', 'data'))
    def print_number_of_filtered_locations(filtered_locations, n_clicks, all_locations):

        # determining which button was pushed
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if trigger == 'locations_clear_filters' and all_locations is not None:
            return f"Znalezionych: {len(all_locations)}"

        if filtered_locations is None:
            if all_locations is not None:
                return f"Znalezionych: {len(all_locations)}"
            raise PreventUpdate

        return f"Znalezionych: {len(filtered_locations)}"

    @dash_app.callback(Output("store-current-location-data", "data"),
                       Input('locations_markers', 'click_feature'),
                       State("store-all-locations-data", "data"))
    def load_current_locations_data(clicked_loc, all_locations):
        if clicked_loc is None:
            return None

        picked_location_id = clicked_loc['properties']['id_lokalizacji']
        curr_location_data = [x for x in all_locations if x['id'] == picked_location_id]

        return curr_location_data[0]

    @dash_app.callback([Output("clicked_loc_name", 'children'),
                        Output('clicked_loc_info', 'children'),
                        Output('clicked_loc_mushrooms', 'children')],
                       Input("store-current-location-data", "data"))
    def load_current_location_card(location_data):
        if location_data is None:
            return None, None, None

        seasonal_mushrooms = fetch_mushrooms_availability(today_month=str(date.today().month))

        for key, value in seasonal_mushrooms.items():
            if value is True:
                seasonal_mushrooms[key] = {
                    "badge": dbc.Badge("W sezonie", color='success'),
                    'color': 'success'
                }
            else:
                seasonal_mushrooms[key] = {
                    'badge': dbc.Badge("Poza sezonem", color='secondary'),
                    'color': 'secondary'
                }

        mushrooms_list = [dbc.ListGroupItem([html.Div([x, " ", seasonal_mushrooms[x]['badge']])],
                                            color=seasonal_mushrooms[x]['color']) for x in location_data['Grzyby']]

        return location_data['Nazwa'], location_data['Opis'], mushrooms_list

    @dash_app.callback(Output("locations_markers", "data"),
                       [Input("locations_clear_filters", "n_clicks"),
                       Input("store-filtered-locations-ids", "data")],
                       Input("store-all-locations-data", "data"))
    def render_filtered_locations_markers(n_clicks, filtered_locations, all_locations):

        # determining which button was pushed
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if trigger == 'locations_clear_filters' and all_locations is not None:
            return dlx.dicts_to_geojson(render_geojson(data=all_locations))

        if filtered_locations is None:
            if all_locations is None:
                raise PreventUpdate
            return dlx.dicts_to_geojson(render_geojson(data=all_locations))

        return dlx.dicts_to_geojson(render_geojson(data=filtered_locations))

    @dash_app.callback(Output("locations_circles", "children"),
                       [Input("locations_clear_filters", "n_clicks"),
                       Input("store-filtered-locations-ids", "data")],
                       Input("store-all-locations-data", "data"))
    def render_filtered_locations_circles(n_clicks, filtered_locations, all_locations):

        # determining which button was pushed
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if trigger == 'locations_clear_filters' and all_locations is not None:
            return [dl.Circle(center=[x['location']['lat'], x['location']['lng']],
                              radius=x['location']['radius_in_meters'],
                              interactive=False)
                    for x in all_locations]

        if filtered_locations is None:
            if all_locations is None:
                raise PreventUpdate
            return [dl.Circle(center=[x['location']['lat'], x['location']['lng']],
                              radius=x['location']['radius_in_meters'],
                              interactive=False)
                    for x in all_locations]

        return [dl.Circle(center=[x['location']['lat'], x['location']['lng']],
                              radius=x['location']['radius_in_meters'],
                              interactive=False)
                    for x in filtered_locations]

    @dash_app.callback([Output('loc_friends_shared_with', 'options'),
                        Output('loc_friends_shared_with', 'value')],
                       Input("store-current-location-data", "data"),
                       State('logged_in_username', 'data'))
    def show_friends_to_share_location(loc_data, un):

        if loc_data is None:
            raise PreventUpdate

        if loc_data['prywatnosc'] == 'my_location':
            opt_disabled = False
        else:
            opt_disabled = True

        shared_with = loc_data['Shared_with']
        all_friends = get_my_friends(user_id=un['un'])

        options = [{'label': x['username'], 'value': x['id'], 'disabled': opt_disabled} for x in all_friends]
        values = [x['id'] for x in shared_with]

        return options, values

    @dash_app.callback([Output('modify-loc-name', 'value'),
                        Output('modify-loc-information', 'value'),
                        Output('modify-loc-mushrooms-list', 'options'),
                        Output('modify-loc-mushrooms-list', 'value')],
                       Input("store-current-location-data", "data"),
                       State('store-all-locations-data', 'data'))
    def modify_location(loc_data, all_loc):

        if loc_data is None:
            raise PreventUpdate

        all_mushrooms_opt = [{'value': x, 'label': x} for x in get_mushrooms_types()]

        return loc_data['Nazwa'], loc_data['Opis'], all_mushrooms_opt, loc_data['Grzyby']

    @dash_app.callback(Output('modify-loc-tab', 'disabled'),
                       Input("store-current-location-data", "data"))
    def hide_modification_tab(loc_data):
        if loc_data is None:
            return True

        if loc_data['prywatnosc'] == 'my_location':
            return False

        return True

    @dash_app.callback([Output('button-modify-loc-submit', 'disabled'),
                        Output('button-save-loc-sharing', 'disabled'),
                        Output('button-delete-loc-submit', 'disabled')],
                       Input("store-current-location-data", "data"))
    def disable_modify_button(loc_data):
        if loc_data is None:
            return True, True, True

        if loc_data['prywatnosc'] == 'my_location':
            return False, False, False

        return True, True, True

    @dash_app.callback(Output('location_info_tabs', 'active_tab'),
                       Input("store-current-location-data", "data"))
    def always_activate_info_tab(loc_data):
        return 0