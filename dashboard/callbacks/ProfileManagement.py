from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def fetch_profile_data():
    moje_dane = {
        "id": 1,
        "Imie": "TestImie",
        "Nazwisko": "TestNazwisko",
        "Email": "test@email.com",
    }
    return moje_dane


def register_callbacks(dash_app):
    @dash_app.callback(
        [
            Output("profile-first-name", "value"),
            Output("profile-last-name", "value"),
            Output("profile-email", "value"),
        ],
        [Input("url", "pathname")],
    )
    def show_profile_info(url):
        if url != "/profil-szczegoly":
            raise PreventUpdate

        profile = fetch_profile_data()

        return profile["Imie"], profile["Nazwisko"], profile["Email"]
