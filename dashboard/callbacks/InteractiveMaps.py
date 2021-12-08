from dash import no_update

from dash.dependencies import Input, Output, State

import dash_leaflet as dl

from dash.exceptions import PreventUpdate

# def register_callbacks(dash_app):
#     @dash_app.callback(Output("text", "children"),
#                        [Input("map", "location_lat_lon_acc")])
#     def update_location(location):
#         return "You are within {} meters of (lat,lon) = ({},{})".format(location[2], location[0], location[1])


def register_callbacks(dash_app):
    @dash_app.callback(Output("main_page_lokalizacje_layer", "children"),
                       [Input("main_map", "click_lat_lng")])
    def map_click(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
