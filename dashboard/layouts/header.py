import dash_bootstrap_components as dbc

navbar_zalogowany = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Przeglądaj", href="lokalizacje-przegladaj#"),
                    dbc.DropdownMenuItem("Dodaj/Usuń lokalizacje", href="lokalizacje-modyfikuj#")
                ],
                nav=True,
                in_navbar=True,
                label="Lokalizacje",
        ),
        dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Przeglądaj", href="grzyby-przegladaj#")
                ],
                nav=True,
                in_navbar=True,
                label="Grzyby",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Szczegóły", href='profil-szczegoly#'),
                dbc.DropdownMenuItem("Znajomi", href="profil-znajomi#"),
            ],
            nav=True,
            in_navbar=True,
            label="Mój Profil",
        ),
        dbc.NavItem(children=[dbc.NavLink("Wyloguj", href='profil-wyloguj#', external_link=True)])
    ],
    brand="Atlas Grzybów",
    brand_href="index",
    color="primary",
    dark=True,
    # fixed='top',
    fluid=True,
    links_left=True,
    expand='lg',
    sticky='top'
)




navbar_niezalogowany = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            children=[
                dbc.NavLink('Rejestracja', href='profil-rejestracja#')
            ]
        ),
        dbc.NavItem(
            children=[
                dbc.NavLink('Logowanie', href='profil-logowanie#')
            ]
        ),
    ],
    brand="Atlas Grzybów",
    brand_href="index#",
    color="primary",
    dark=True,
    # fixed='top',
    fluid=True,
    links_left=True,
    expand='lg',
    sticky='top'
)