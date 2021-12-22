import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

mushroom_imgs = dbc.Carousel(
        id='curr_mushroom_imgs',
        items=[],
        controls=False,
        indicators=True,
        interval=None
)

dropdown_options = html.Div([dcc.Dropdown(
        id='dropdown_mushroom_option',
        options=[],
        placeholder="Wyszukaj z listy..."
)])

mushroom_card = dbc.Card(
    [

        html.H1(id='mushroom_informal_name_view'),
        html.P(id='mushroom_formal_name_view',
               className="lead"),
        mushroom_imgs,
        dbc.CardBody(
            [
                html.Div(
                    id='mushroom_info',
                    className="py-4",
                )
            ]
        ),
    ]
)

main_page = dbc.Container([
    dcc.Store(id='mushrooms_viewer_data'),
    dcc.Store(id='mushrooms_viewer_current_view'),

    dbc.Row([
        dbc.Col([dropdown_options], xl=4, lg=6, md=12, sm=12)
    ], style={"margin": '1rem'}, className="g-0", justify="center",),
    dbc.Row([
        dbc.Col([
            dbc.Button("Poprzedni", id='previous_mushroom', size='lg')
        ], width='auto'),
        dbc.Col([
            dbc.Button("Następny", id='next_mushroom', size='lg')
        ], width='auto')
    ], justify="center", style={"margin": '1rem'}),
    dbc.Row([
        dbc.Col([
            mushroom_card
        ], xl=4, lg=4)
    ], justify="center",)
], fluid=True)
