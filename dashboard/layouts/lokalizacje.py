import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_leaflet as dl

MAP_STYLE = {'width': '100%', 'height': '25rem'}

locations_map = dl.Map([
    dl.TileLayer(),
    dl.GeoJSON(data=[], id='locations_markers'),
    dl.LocateControl(options={'locateOptions'       : {'enableHighAccuracy': True},
                              'keepCurrentZoomLevel': False,
                              'showPopup'           : False})
], center=[52.15, 19.7], style=MAP_STYLE, id='locations_map')

clicked_loc_card = dbc.Card([
    html.H2([], id='clicked_loc_name', className='py-1'),
    html.Hr(),
    dbc.CardBody(
            [
                html.P([], id='clicked_loc_info', className='py-1'),
                dbc.ListGroup([], id='clicked_loc_mushrooms')
            ]
        ),
])

main_page = dbc.Container([
    dcc.Store(id='store_for_main_page_lokalizacje'),
    dcc.Store(id='store-all-locations-data'),
    dcc.Store(id='store-filtered-locations-ids'),
    dcc.Store(id='store-current-location-data'),
    dbc.Row(dbc.Col(html.Div([locations_map]))),
    dbc.Row(dbc.Col(dbc.Button('Pokaż filtry lokalizacji', id='locations_show_filters'))),
    dbc.Offcanvas([
        dbc.Row(dbc.Col(
                html.Div(
                        dbc.Button("Zastosuj filtry", id='locations_apply_filters', color='success'),
                className='py-1'))),
        dbc.Row(dbc.Col(
                html.Div(
                        dbc.Button("Wyczyść filtry", id='locations_clear_filters'),
                        className='py-1'))),
        dbc.Row(dbc.Col([
            html.Div(
                    [
                        dbc.Label(id='locations_filtered_number'),
                    ], className="py-4"
            )
        ])),
        dbc.Row(dbc.Col([
            html.Div(
                    [
                        dbc.Label("Pokaż lokalizacje:"),
                        dbc.Checklist(
                                options=[
                                    {"label": "Moje", "value": 'my_location'},
                                    {"label": "Udostępnione", "value": 'shared_with_me'},
                                    {"label": "Publiczne", "value": 'public'},
                                ],
                                value=['public', 'my_location', 'shared_with_me'],
                                id="locations_filters_loctypes",
                                switch=True,
                        ),
                    ], className="py-4"
            )
        ])),
        dbc.Row(dbc.Col([
            html.Div(
                    [
                        dbc.Label("Musi zawierać:"),
                        dbc.Checklist(
                                options=[],
                                value=[],
                                id="locations_filters_mushroomtypes",
                                switch=False,
                        ),
                    ], className="py-4"
            )
        ]))
    ],
            id='locations_filters',
            title='Filtry lokalizacji',
            is_open=False
    ),
    dbc.Accordion([
        dbc.AccordionItem([
            clicked_loc_card
        ], title="Informacje o lokalizacji"),
        dbc.AccordionItem([
            dbc.Row(id='weather_forecast_placeholder')
        ], title="Prognoza pogody"),
        dbc.AccordionItem([
        ], title="Udostępnij znajomym")
    ], start_collapsed=True),
], fluid=True)

manage = dbc.Container([
    dbc.Row(dbc.Col(html.H1("manage lokalizacje")))
])
