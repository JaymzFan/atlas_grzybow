import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_leaflet as dl

MAP_STYLE = {'width': '100%', 'height': '25rem'}

locations_map = dl.Map([
    dl.TileLayer(updateWhenZooming=False),
    dl.GeoJSON(children=[], id='locations_circles'),
    dl.GeoJSON(data=[], id='locations_markers'),
    dl.LocateControl(options={'locateOptions'       : {'enableHighAccuracy': True},
                              'keepCurrentZoomLevel': True,
                              'showPopup'           : False})
], center=[52.15, 19.7], style=MAP_STYLE, id='locations_map')

clicked_loc_card = dbc.Card([
    html.H2([], id='clicked_loc_name',
            #className='py-1',
            style={'margin-top': '0.2rem', 'margin-left': '1rem'}),
    #html.Hr(),
    dbc.CardBody(
            [
                html.P([], id='clicked_loc_info'),# className='py-1'),
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
            dbc.Textarea(id='modify-loc-information', style={'height': '8rem'})
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Promień obszaru w metrach"),
        dbc.Col([dbc.Input(type='number', id='modify-loc-radius-in-meters',
                           debounce=True)])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Występujące grzyby:"),
        dbc.Col([
           dcc.Dropdown(options=[], value=[], multi=True, id='modify-loc-mushrooms-list',
                        placeholder="Wybierz z listy",
                        style=
                            {'color'           : '#212121',
                             'background-color': '#212121',
                             'height': '6rem'
                             }
                        )
        ])
    ]),
    dbc.Row([
        dbc.Button("Zapisz", id='button-modify-loc-submit', n_clicks=0,
                   style={'margin-top': '4rem'})
    ]),
    dbc.Row([
        dbc.Alert('Dane lokalizacji zostały zaktualizowane',
                  id='loc_modify_data_alert',
                  fade=True,
                  dismissable=True,
                  is_open=False,
                  duration=3000)
    ]),
    dbc.Row([
        dbc.Button("Usuń lokalizację", color='danger', id='button-delete-loc-submit', n_clicks=0,
                   style={'margin-top': '2rem'})
    ]),
    dbc.Row([
        dbc.Alert('Lokalizacja została usunięta z bazy danych',
                  id='loc_delete_locations_alert',
                  fade=True,
                  dismissable=True,
                  is_open=False,
                  duration=3000)
    ]),
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
                    ], className="py-1"
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
    dbc.Row(dbc.Col(html.Div([locations_map]), xl=8, lg=8, md=12, sm=12), justify="center"),
    dbc.Row(dbc.Col(dbc.Button('Pokaż filtry lokalizacji', id='locations_show_filters', style={'width': "100%", 'margin-top': '1rem'}), xl=8, lg=8, md=12, sm=12), justify="center"),
    filtry_canvas,
    dbc.Row(dbc.Col([
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Tabs([
                    dbc.Tab(clicked_loc_card,
                            label='Szczegóły'),
                    dbc.Tab(modify_loc_card,
                            label='Modyfikuj',
                            id='modify-loc-tab'),
                ])
            ], title="Informacje o lokalizacji", id='location_info_tabs'),
            dbc.AccordionItem([
                dbc.Row(id='weather_forecast_placeholder')
            ], title="Prognoza pogody"),
            dbc.AccordionItem([
                dbc.Row(dbc.Col(dbc.Button('Zapisz zmiany', id='button-save-loc-sharing'))),
                dbc.Row(dbc.Col(dbc.Alert("Zmiany zostały zapisane", id='alert-setting-ppl-to-share-loc', is_open=False, duration=3000))),
                dbc.Checklist(
                        id='loc_friends_shared_with',
                        options=[],
                        value=[], labelStyle={"display": "block"}
                )
            ], title="Udostępnij znajomym")
        ], start_collapsed=True)
    ], xl=8, lg=8, md=12, sm=12), justify="center", style={'margin-top': '1rem'}),
], fluid=True)


add_new_loc_card = dbc.Form([
    dbc.Row([
        dbc.Label("Położenie"),
        dbc.Col([
        ], id='add_new_loc_info')
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Promień obszaru w metrach"),
        dbc.Col([dbc.Input(type='number', id='loc-addnew-radius-in-meters',
                           debounce=True)])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Nazwa"),
        dbc.Col([
            dbc.Input(type='text', id='addnew-loc-name', debounce=True)
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Opis"),
        dbc.Col([
            dbc.Textarea(id='addnew-loc-information', style={'height': '8rem'})
        ], className="mb-3")
    ]),
    dbc.Row([
        dbc.Label("Występujące grzyby:"),
        dbc.Col([
            dcc.Dropdown(options=[], value=[], multi=True, id='addnew-loc-mushrooms-list',
                         placeholder="Wybierz z listy",
                         style=
                         {'color'           : '#212121',
                          'background-color': '#212121',
                          'height': '6rem'
                          }
                         )
        ])
    ]),
    dbc.Row(dbc.Col([
        dbc.Button("Zapisz", id='button-addnew-loc-submit', n_clicks=0, style={'width': '100%',
                                                                               'margin-top': '2rem'})
    ])),
    dbc.Row([
        dbc.Alert('Lokalizacja została dodana do bazy danych',
                  id='loc_add_new_locations_alert',
                  fade=True,
                  dismissable=True,
                  is_open=False,
                  duration=3000)
    ]),
])

add_new_locations_map = dl.Map([
                dl.TileLayer(),
                dl.LayerGroup(id="add-new-location-map-layer"),
                dl.GeoJSON(children=[], id='add-new-location-circle'),
                dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True},
                                          'keepCurrentZoomLevel': False,
                                          'showPopup': False})
            ], id='add-new-location-map', center=[52.15, 19.7], style=MAP_STYLE)

manage = dbc.Container([
    dbc.Row(dbc.Col([
        add_new_locations_map
    ], xl=8, lg=8, md=12, sm=12, width=12, align='center'), justify='center'),
    dbc.Row(dbc.Col([
        add_new_loc_card
    ], xl=8, lg=8, md=12, sm=12), justify='center')
], fluid=True)
