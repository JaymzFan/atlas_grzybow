import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

main_page2 = html.Div([
    html.H1("main_page grzyby")
])

main_page = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("asdf")),
        dbc.Col(html.Div("aasdfff"))
    ]),
    dbc.Row(dbc.Col(html.Div("12345"), width="auto"))
])
