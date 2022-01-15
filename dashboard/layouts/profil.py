import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

szczegoly = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Label("Imię", width=3),
                dbc.Col(dbc.Input(type="text", id="profile-first-name")),
            ]
        ),
        dbc.Row(
            [
                dbc.Label("Nazwisko", width=3),
                dbc.Col(dbc.Input(type="text", id="profile-last-name")),
            ]
        ),
        dbc.Row(
            [
                dbc.Label("Email", width=3),
                dbc.Col(dbc.Input(type="email", id="profile-email")),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button("Zapisz", id="button-submit-user-profile")),
            ]
        ),
    ]
)

znajomi = dbc.Container(
    [
        dcc.Store(id="znajomi-storage"),
        dbc.Row([dbc.Col([html.H2(id="current_user_welcome")])]),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [dbc.Row(dbc.Col(id="lista-znajomych"))]
                                            )
                                        ]
                                    )
                                ],
                                title="Lista znajomych",
                            ),
                            dbc.AccordionItem(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                id="dropdown_friends_to_add",
                                                                                options=[],
                                                                                placeholder="Wyszukaj użytkownika ...",
                                                                                style={
                                                                                    "height": "2.5rem",
                                                                                    "color": "#212121",
                                                                                    "background-color": "#212121",
                                                                                    "Select-value-label-color": "#3333333",
                                                                                },
                                                                                multi=False,
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            dbc.Col(
                                                                dbc.Button(
                                                                    "Dodaj do listy",
                                                                    id="add_friend-submit",
                                                                    color="success",
                                                                    n_clicks=0,
                                                                    size="lg",
                                                                    style={
                                                                        "margin-top": "3rem"
                                                                    },
                                                                )
                                                            ),
                                                            dbc.Row(
                                                                dbc.Alert(
                                                                    "Dodano do listy",
                                                                    id="alert-added-friend",
                                                                    is_open=False,
                                                                    color="primary",
                                                                    duration=4000,
                                                                )
                                                            ),
                                                            dbc.Row(
                                                                dbc.Col(
                                                                    html.Div(
                                                                        id="add_friend_status"
                                                                    )
                                                                )
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                title="Dodaj do grona znajomych",
                            ),
                            dbc.AccordionItem(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    dcc.Dropdown(
                                                                        id="dropdown_friends_to_remove",
                                                                        options=[],
                                                                        placeholder="Wybierz z listy",
                                                                        style={
                                                                            "height": "2.5rem",
                                                                            "color": "#212121",
                                                                            "background-color": "#212121",
                                                                            "Select-value-label-color": "#3333333",
                                                                        },
                                                                        multi=False,
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dbc.Button(
                                                                    "Usuń znajomego z listy",
                                                                    color="danger",
                                                                    id="remove_friend-submit",
                                                                    size="lg",
                                                                    n_clicks=0,
                                                                    style={
                                                                        "margin-top": "3rem"
                                                                    },
                                                                )
                                                            )
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        dbc.Alert(
                                                            "Usunięto z listy",
                                                            id="alert-removed-friend",
                                                            is_open=False,
                                                            color="primary",
                                                            duration=4000,
                                                        )
                                                    ),
                                                    dbc.Row(
                                                        dbc.Col(
                                                            html.Div(
                                                                id="remove_friend_status"
                                                            )
                                                        )
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                title="Usuń z grona znajomych",
                            ),
                        ],
                        start_collapsed=True,
                    )
                ]
            )
        ),
    ],
    fluid=False,
)

zaloguj = html.Div([html.H1("Profil zaloguj")])
