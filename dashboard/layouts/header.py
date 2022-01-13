import dash_bootstrap_components as dbc
import dash_core_components as dcc

navbar_zalogowany = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Przeglądaj", href="lokalizacje-przegladaj#"),
                    dbc.DropdownMenuItem("Dodaj lokalizację", href="lokalizacje-modyfikuj#")
                ],
                nav=True,
                in_navbar=True,
                label="Lokalizacje"
        ),
        dbc.NavItem(dbc.NavLink("Grzyby", href="grzyby-przegladaj#")),
        dbc.NavItem(dbc.NavLink("Znajomi", href="profil-znajomi#")),
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
    sticky='top', id='navbar_zalogowany'
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