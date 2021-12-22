import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


acc_create_username = dbc.Row([
            dbc.Label("Nazwa użytkownika"),
            dcc.Input(id='username', type='text', placeholder='username', maxLength=25),
            dbc.FormText(
                    "Wymagane. Maksymalnie 25 znaków",
                    color="secondary",
            )
        ], className="mb-3")

acc_create_email = dbc.Row([
            dbc.Label("Email",  html_for="example-email"),
            dcc.Input(id='useremail', placeholder='email', type='email', maxLength=50),
            dbc.FormText(
                    "Wymagane. Maksymalnie 50 znaków",
                    color="secondary",
            )
        ], className="mb-3")

acc_create_password = dbc.Row([
            dbc.Label("Hasło"),
            dcc.Input(id='password', placeholder='hasło', type='password'),
        ], className="mb-3")

acc_create_button = dbc.Row([
    dbc.Button('Zarejestruj', id='submit-val', n_clicks=0)
    ])

acc_create_already_exist_notification = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Błąd!")),
        dbc.ModalBody("Użytkownik już istnieje!"),
        dbc.ModalFooter("Użyj innej nazwy użytkownika lub email")
    ], id="acc_already_exists_modal", is_open=False, centered=True)
])


create_account = dbc.Form([
    dcc.Location(id='url-rejestracja', refresh=True),
    acc_create_username,
    acc_create_email,
    acc_create_password,
    acc_create_button,
    acc_create_already_exist_notification
])

create_account = dbc.Container([create_account])

# create_account2 = html.Div([
#     dcc.Location(id='url-rejestracja', refresh=True),
#     dbc.Container([
#         dbc.Row(
#                 dbc.Col(
#                         html.H1('Rejestracja'),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#         dbc.Row(
#                 dbc.Col(
#                         dcc.Input(id='username', type='text', placeholder='username', maxLength=25),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#         dbc.Row(
#                 dbc.Col(
#                         dcc.Input(id='useremail', placeholder='email', type='email', maxLength=50),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#         dbc.Row(
#                 dbc.Col(
#                         dcc.Input(id='password', placeholder='hasło', type='password'),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#         dbc.Row(
#                 dbc.Col(
#                         html.Button('Zarejestruj', id='submit-val', n_clicks=0),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#         dbc.Row(
#                 dbc.Col(
#                         html.Div(id='container-button-basic'),
#                         width={'size': 6, "offset": 3}
#                 )
#         ),
#     ])
# ])


acc_login_username = dbc.Row([
            dbc.Label("Nazwa użytkownika"),
            dcc.Input(id='uname-box', type='text', placeholder='username', maxLength=25),
        ], className="mb-3")

acc_login_password = dbc.Row([
            dbc.Label("Hasło"),
            dcc.Input(id='pwd-box', placeholder='hasło', type='password'),
        ], className="mb-3")

acc_login_button = dbc.Row([
    dbc.Button('Zaloguj', id='login-button', n_clicks=0)
    ])

acc_login_incorrect_credentials = html.Div(children='', id='output-state')


login_account = dbc.Form([
    dcc.Location(id='url_login', refresh=True),
    dcc.Location(id='url_logout', refresh=True),
    acc_login_username,
    acc_login_password,
    acc_login_button,
    acc_login_incorrect_credentials
])

login_account = dbc.Container([login_account])
login = login_account
#
#
# login = html.Div([
#     dcc.Location(id='url_login', refresh=True),
#     dcc.Location(id='url_logout', refresh=True),
#     dbc.Container([
#         dbc.Row(
#             dbc.Col(
#                 html.H2('''Logowanie''', id='h1', style={'align': "center"}),
#                 align='center',
#                 width={'size': 6, "offset": 3}
#             ),
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dcc.Input(placeholder='username', type='text', id='uname-box'),
#                 width={'size': 6, "offset": 3}
#             ),
#         ),
#         dbc.Row(
#             dbc.Col(
#                 dcc.Input(placeholder='hasło', type='password', id='pwd-box'),
#                 width={'size': 6, "offset": 3}
#             ),
#         ),
#         dbc.Row(
#             dbc.Col(
#                 html.Button(children='Logowanie', n_clicks=0, type='submit', id='login-button'),
#                 width={'size': 6, "offset": 3}
#             ),
#         ),
#         dbc.Row(
#             dbc.Col(
#                 html.Div(children='', id='output-state'),
#                 width={'size': 6, "offset": 3}
#             )
#         )
#     ])
# ]) #end div

already_exists = html.Div([
    html.H2("Już posiadasz konto? Przejdź do strony logowania")
])
