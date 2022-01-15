from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        dbc.Container(
            [
                dcc.Store(id="logged_in_username", storage_type="session"),
                dbc.Row(dbc.Col(html.Div([html.Div(id="header-content")]))),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                dcc.Location(id="url", refresh=True),
                                html.Div(id="page-content"),
                            ]
                        )
                    )
                ),
            ],
            fluid=True,
        )
    ]
)
