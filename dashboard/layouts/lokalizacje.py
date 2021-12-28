import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_leaflet as dl

MAP_STYLE = {'width': '100%', 'height': '25rem'}

locations_map = dl.Map([
    dl.TileLayer(updateWhenZooming=False),
    dl.GeoJSON(data=[], id='locations_markers'),
    dl.LocateControl(options={'locateOptions'       : {'enableHighAccuracy': True},
                              'keepCurrentZoomLevel': True,
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

modify_loc_card = dbc.Form([
    dbc.Row([
        dbc.Label("Nazwa"),
        dbc.Col([
            dbc.Input(type='text', id='modify-loc-name')
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Opis"),
        dbc.Col([
            dbc.Textarea(id='modify-loc-information')
        ])
    ]),
    dbc.Row([
        dbc.Label("Występujące grzyby:"),
        dbc.Col([
           dcc.Dropdown(options=[], value=[], multi=True, id='modify-loc-mushrooms-list',
                        style=
                            {'color'           : '#212121',
                             'background-color': '#212121',
                             }
                        )
        ])
    ]),
    dbc.Row([
        dbc.Button("Zapisz", id='button-modify-loc-submit', n_clicks=0,
                   style={'margin-top': '2rem'})
    ]),
    dbc.Row([
        dbc.Button("Usuń lokalizację", color='danger', id='button-delete-loc-submit', n_clicks=0,
                   style={'margin-top': '2rem'})
    ])
])


filtry_canvas = dbc.Offcanvas([
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
                        dbc.Button('Zaznacz grzyby sezonowe', id='button-mark-sesonal-mushrooms', className='py-1'),
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
    )

main_page = dbc.Container([
    dcc.Store(id='store_for_main_page_lokalizacje'),
    dcc.Store(id='store-all-locations-data'),
    dcc.Store(id='store-filtered-locations-ids'),
    dcc.Store(id='store-current-location-data'),
    dbc.Row(dbc.Col(html.Div([locations_map]))),
    dbc.Row(dbc.Button('Pokaż filtry lokalizacji', id='locations_show_filters')),
    filtry_canvas,
    dbc.Accordion([
        dbc.AccordionItem([
            dbc.Tabs([
                dbc.Tab(clicked_loc_card,
                        label='Info',
                        active_tab_style={"textTransform": "uppercase"}),
                dbc.Tab(modify_loc_card,
                        label='Modyfikuj',
                        active_tab_style={"textTransform": "uppercase"},
                        id='modify-loc-tab'),
            ])
        ], title="Informacje o lokalizacji", id='location_info_tabs'),
        dbc.AccordionItem([
            dbc.Row(id='weather_forecast_placeholder')
        ], title="Prognoza pogody"),
        dbc.AccordionItem([
            dbc.Row(dbc.Col(dbc.Button('Zapisz zmiany', id='button-save-loc-sharing'))),
            dbc.Checklist(
                id='loc_friends_shared_with',
                options=[],
                value=[], labelStyle={"display": "block"}
            )
        ], title="Udostępnij znajomym")
    ], start_collapsed=True),
], fluid=True)


add_new_loc_card = dbc.Form([
    dbc.Row([
        dbc.Label("Położenie"),
        dbc.Col([
        ], id='add_new_loc_info')
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Nazwa"),
        dbc.Col([
            dbc.Input(type='text', id='addnew-loc-name')
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Opis"),
        dbc.Col([
            dbc.Textarea(id='addnew-loc-information')
        ])
    ]),
    dbc.Row([
        dbc.Label("Występujące grzyby:"),
        dbc.Col([
            dcc.Dropdown(options=[], value=[], multi=True, id='addnew-loc-mushrooms-list',
                         style=
                         {'color'           : '#212121',
                          'background-color': '#212121',
                          }
                         )
        ])
    ]),
    dbc.Row([
        dbc.Button("Zapisz", id='button-addnew-loc-submit', n_clicks=0)
    ])
])

add_new_locations_map = dl.Map([
                dl.TileLayer(),
                dl.LayerGroup(id="add-new-location-map-layer"),
                dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True},
                                          'keepCurrentZoomLevel': False,
                                          'showPopup': False})
            ], id='add-new-location-map', center=[52.15, 19.7], style=MAP_STYLE)

manage = dbc.Container([
    dcc.Store(id='store-all-locations-addnew-data'),
    dbc.Row(dbc.Col([
        add_new_locations_map
    ], width=12, align='center')),
    dbc.Row(dbc.Col([
        add_new_loc_card
    ]))
], fluid=True)
