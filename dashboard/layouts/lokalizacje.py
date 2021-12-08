import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_leaflet as dl
MAP_STYLE = {'width': '100%', 'height': '25rem'}
main_page = dbc.Container([
    dcc.Store(id='store_for_main_page_lokalizacje'),
    dbc.Row(dbc.Col(html.H1("main_page lokalizacje"), width='auto')),
    dbc.Row(dbc.Col(html.Div(
            [dl.Map([
                dl.TileLayer(),
                dl.LayerGroup(id="main_page_lokalizacje_layer"),
                dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True},
                                          'keepCurrentZoomLevel': False,
                                          'showPopup': False})
            ], id='main_map', center=[52.15, 19.7], style=MAP_STYLE)])))
], fluid=True)

manage = dbc.Container([
    dbc.Row(dbc.Col(html.H1("manage lokalizacje")))
])
