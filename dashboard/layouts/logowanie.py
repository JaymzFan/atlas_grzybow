import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

create_account = html.Div([
    dcc.Location(id='url-rejestracja', refresh=True),
    dbc.Container([
        dbc.Row(
                dbc.Col(
                        html.H1('Rejestracja'),
                        width={'size': 6, "offset": 3}
                )
        ),
        dbc.Row(
                dbc.Col(
                        dcc.Input(id='username', type='text', placeholder='username', maxLength=25),
                        width={'size': 6, "offset": 3}
                )
        ),
        dbc.Row(
                dbc.Col(
                        dcc.Input(id='useremail', placeholder='email', type='email', maxLength=50),
                        width={'size': 6, "offset": 3}
                )
        ),
        dbc.Row(
                dbc.Col(
                        dcc.Input(id='password', placeholder='hasło', type='password'),
                        width={'size': 6, "offset": 3}
                )
        ),
        dbc.Row(
                dbc.Col(
                        html.Button('Zarejestruj', id='submit-val', n_clicks=0),
                        width={'size': 6, "offset": 3}
                )
        ),
        dbc.Row(
                dbc.Col(
                        html.Div(id='container-button-basic'),
                        width={'size': 6, "offset": 3}
                )
        ),
    ])
])

login = html.Div([
    dcc.Location(id='url_login', refresh=True),
    dcc.Location(id='url_logout', refresh=True),
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H2('''Logowanie''', id='h1', style={'align': "center"}),
                align='center',
                width={'size': 6, "offset": 3}
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Input(placeholder='username', type='text', id='uname-box'),
                width={'size': 6, "offset": 3}
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Input(placeholder='hasło', type='password', id='pwd-box'),
                width={'size': 6, "offset": 3}
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Button(children='Logowanie', n_clicks=0, type='submit', id='login-button'),
                width={'size': 6, "offset": 3}
            ),
        ),
        dbc.Row(
            dbc.Col(
                html.Div(children='', id='output-state'),
                width={'size': 6, "offset": 3}
            )
        )
    ])
]) #end div

already_exists = html.Div([
    html.H2("Już posiadasz konto? Przejdź do strony logowania")
])
