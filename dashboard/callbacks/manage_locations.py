import dash_leaflet as dl

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


from config import get_db_uri

from sqlalchemy import create_engine

from database.DatabaseInterface import DatabaseSessionManager, DatabaseFacade


def modify_existing_location(loc_id: int, params, mush_informal_names):
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    db.locations.update_location(object_id=loc_id, **params)

    # get mushrooms ids
    mush_ids = []
    for x in mush_informal_names[0]:
        grzyb = db.mushrooms.fetch_all_mushrooms(filters=dict(nazwa_nieformalna=x))
        mush_ids.append(grzyb[0].__dict__["id"])

    db.set_mushrooms_to_location(location_id=loc_id, mushroom_ids=mush_ids)
    return True


def delete_existing_location(loc_id: int):
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    # removing mushrooms association and assigned shared friends
    db.set_mushrooms_to_location(location_id=loc_id, mushroom_ids=[])
    set_shared_with_to_location(loc_id=loc_id, friends_ids=[])

    loc_to_remove = db.locations.fetch_all_locations(filters=dict(id=loc_id))
    db.locations.session.remove_objects(objects=loc_to_remove)

    return True


def set_shared_with_to_location(loc_id, friends_ids):
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    db.set_shared_with_to_location(location_id=loc_id, friends_ids=friends_ids)
    return True


def get_mushrooms_by_names(mushrooms_informal_names):
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    all_mushrooms = []
    for mush in mushrooms_informal_names:
        mushroom = db.mushrooms.fetch_all_mushrooms(
            filters=dict(nazwa_nieformalna=mush)
        )[0]
        all_mushrooms.append(mushroom)

    return all_mushrooms


def add_new_location(
    owner_id, nazwa, opis, center_lat, center_lon, radius_in_meters, mushrooms_names
):
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    all_mushrooms = db.mushrooms.fetch_all_mushrooms()

    db.locations.add_location(
        owner_id=owner_id,
        nazwa=nazwa,
        opis=opis,
        center_lat=center_lat,
        center_lon=center_lon,
        radius_in_meters=radius_in_meters,
        loc_mushrooms=all_mushrooms,
        czy_publiczna=0,
    )

    return True


def get_mushrooms_types():
    db = DatabaseFacade(
        session_manager=DatabaseSessionManager(db_engine=create_engine(get_db_uri()))
    )

    typy_grzybow = []
    for x in db.fetch_mushrooms_data():
        typy_grzybow.append(x["MushroomNameInFormal"])

    return typy_grzybow


def register_callbacks(dash_app):
    @dash_app.callback(
        Output("add-new-location-map-layer", "children"),
        [Input("add-new-location-map", "click_lat_lng")],
    )
    def map_click(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        return [
            dl.Marker(
                position=click_lat_lng,
                children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)),
            )
        ]

    @dash_app.callback(
        Output("add_new_loc_info", "children"),
        [Input("add-new-location-map", "click_lat_lng")],
    )
    def get_curr_location(click_lat_lng):
        if click_lat_lng is None:
            raise PreventUpdate
        click_lat_lng = [round(x, ndigits=1) for x in click_lat_lng]
        return str(click_lat_lng)

    @dash_app.callback(
        Output("loc_add_new_locations_alert", "is_open"),
        Input("button-addnew-loc-submit", "n_clicks"),
        [
            State("addnew-loc-mushrooms-list", "value"),
            State("addnew-loc-information", "value"),
            State("addnew-loc-name", "value"),
            State("add-new-location-map", "click_lat_lng"),
            State("logged_in_username", "data"),
            State("loc-addnew-radius-in-meters", "value"),
        ],
    )
    def addnew_location_to_database(
        n_clicks,
        mushrooms_names,
        loc_opis,
        loc_nazwa,
        loc_center,
        loggedin_user,
        radius,
    ):

        if n_clicks == 0:
            raise PreventUpdate

        if radius is None:
            raise PreventUpdate

        if radius < 0:
            raise PreventUpdate

        if loc_nazwa is None:
            raise PreventUpdate

        if loc_center is None:
            raise PreventUpdate

        add_new_location(
            owner_id=loggedin_user["id"],
            nazwa=loc_nazwa,
            opis=loc_opis,
            center_lon=loc_center[1],
            center_lat=loc_center[0],
            radius_in_meters=radius,
            mushrooms_names=mushrooms_names,
        )

        return True

    @dash_app.callback(
        Output("addnew-loc-mushrooms-list", "options"), Input("url", "pathname")
    )
    def add_new_loc_mushrooms_options(url):
        if url != "/lokalizacje-modyfikuj":
            raise PreventUpdate

        return [{"label": x, "value": x} for x in get_mushrooms_types()]

    @dash_app.callback(
        Output("loc_modify_data_alert", "is_open"),
        Input("button-modify-loc-submit", "n_clicks"),
        [
            State("store-current-location-data", "data"),
            State("modify-loc-mushrooms-list", "value"),
            State("modify-loc-information", "value"),
            State("modify-loc-name", "value"),
            State("modify-loc-radius-in-meters", "value"),
        ],
    )
    def modify_and_popup_alert_successful(
        n_clicks, curr_loc_data, mushrooms, opis, nazwa, radius
    ):
        if n_clicks == 0:
            raise PreventUpdate
        curr_loc_id = curr_loc_data["id"]

        modify_existing_location(
            loc_id=curr_loc_id,
            params=dict(nazwa=nazwa, opis=opis, radius_in_meters=radius),
            mush_informal_names=[mushrooms],
        )
        return True

    @dash_app.callback(
        Output("loc_delete_locations_alert", "is_open"),
        Input("button-delete-loc-submit", "n_clicks"),
        [State("store-current-location-data", "data")],
    )
    def popup_alert_delete_successful(n_clicks, curr_loc_data):
        if n_clicks == 0:
            raise PreventUpdate
        curr_loc_id = curr_loc_data["id"]

        delete_existing_location(loc_id=curr_loc_id)
        return True

    @dash_app.callback(
        Output("alert-setting-ppl-to-share-loc", "is_open"),
        Input("button-save-loc-sharing", "n_clicks"),
        [
            State("loc_friends_shared_with", "value"),
            State("store-current-location-data", "data"),
        ],
    )
    def set_to_whom_curr_locations_should_be_shared(
        n_clicks, friends_to_share_with, curr_loc
    ):
        if n_clicks == 0:
            raise PreventUpdate
        if curr_loc is None:
            raise PreventUpdate

        curr_loc_id = curr_loc["id"]
        set_shared_with_to_location(
            loc_id=curr_loc_id, friends_ids=friends_to_share_with
        )
        return True

    @dash_app.callback(
        Output("add-new-location-circle", "children"),
        Input("loc-addnew-radius-in-meters", "value"),
        State("add-new-location-map", "click_lat_lng"),
    )
    def render_circle(circle_radius, click_lat_lng):

        if circle_radius is None:
            raise PreventUpdate

        if circle_radius < 0:
            raise PreventUpdate

        if click_lat_lng is None:
            raise PreventUpdate

        return [
            dl.Circle(center=click_lat_lng, radius=circle_radius, interactive=False)
        ]
