from dash import callback_context

from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate

import dash_html_components as html
import dash_bootstrap_components as dbc

def load_mushrooms_data():
    demo_dane = [
        {
            'MushroomNameFormal'  : "Grzyb1",
            'MushroomNameInFormal': "Nieformalna Grzyb1",
            'MushroomInfo'        : {'Opis': "Opis Grzyba1",
                                     "Cechy": "Cechy",
                                     "Cechy inne": "Cechy innne"},
            'Photos'              : [
                './static/images_mushrooms/Boczniak1.png',
                './static/images_mushrooms/Boczniak1.png',
                './static/images_mushrooms/Boczniak1.png'
            ],
            'Toxic': False
        },
        {
            'MushroomNameFormal'  : "Grzyb2",
            'MushroomNameInFormal': "Nieformalna Grzyb2",
            'MushroomInfo'        : {'opis': "Opis Grzyba2"},
            'Photos'              : [
                './static/images_mushrooms/Boczniak2.png',
                './static/images_mushrooms/Boczniak2.png',
                './static/images_mushrooms/Boczniak2.png'
            ],
            'Toxic': True
        },
        {
            'MushroomNameFormal'  : "Grzyb3",
            'MushroomNameInFormal': "Nieformalna Grzyb3",
            'MushroomInfo'        : {'opis': "Opis Grzyba3"},
            'Photos'              : [
                './static/images_mushrooms/Boczniak3.png',
                './static/images_mushrooms/Boczniak3.png',
                './static/images_mushrooms/Boczniak3.png'
            ],
            'Toxic': False
        },
        {
            'MushroomNameFormal'  : "Grzyb4",
            'MushroomNameInFormal': "Nieformalna Grzyb4",
            'MushroomInfo'        : {'opis': "Opis Grzyba4"},
            'Photos'              : [
                './static/images_mushrooms/Boczniak4.png',
                './static/images_mushrooms/Boczniak4.png',
                './static/images_mushrooms/Boczniak4.png'
            ],
            'Toxic': False
        }
    ]

    return demo_dane


def register_callbacks(dash_app):

    @dash_app.callback(Output("mushrooms_viewer_data", "data"),
                       Input('url', 'pathname'))
    def store_mushroom_state_info(url):
        if url != '/grzyby-przegladaj':
            raise PreventUpdate

        # ToDO: posortuj liste grzybow po nazwie
        return load_mushrooms_data()

    @dash_app.callback(Output("mushrooms_viewer_current_view", "data"),
                       [Input('mushrooms_viewer_data', 'data'),
                        Input('previous_mushroom', 'n_clicks'),
                        Input('next_mushroom', 'n_clicks'),
                        Input('dropdown_mushroom_option', 'value')
                        ],
                       State('mushrooms_viewer_current_view', 'data'))
    def pick_current_mushroom_info(data, prev_click, next_click, dropdown, curr_data):
        if data is None:
            return None, None

        how_many_available = len(data)

        # determining which button was pushed
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if curr_data is None:
            curr_viewed = 0
        else:
            curr_viewed = curr_data[0]

        if trigger == 'previous_mushroom':
            curr_viewed = curr_viewed - 1
        elif trigger == 'next_mushroom':
            curr_viewed = curr_viewed + 1
        elif trigger == 'dropdown_mushroom_option':
            if dropdown is None:
                raise PreventUpdate
            curr_viewed = dropdown

        if curr_viewed >= how_many_available:
            curr_viewed = how_many_available - 1
        elif curr_viewed <= 0:
            curr_viewed = 0

        return curr_viewed, data[curr_viewed]

    @dash_app.callback(Output("dropdown_mushroom_option", "value"),
                       [Input('mushrooms_viewer_data', 'data'),
                        Input('previous_mushroom', 'n_clicks'),
                        Input('next_mushroom', 'n_clicks')])
    def clear_dropdown_value(data, prev_click, next_click):

        return None

    @dash_app.callback([Output("previous_mushroom", "disabled"),
                        Output("next_mushroom", "disabled")],
                       Input('mushrooms_viewer_current_view', 'data'),
                       State('mushrooms_viewer_data', 'data'))
    def control_disabling_buttons(curr_data, all_data):
        if all_data is None:
            return False, False

        how_many_available = len(all_data)

        # determining which button was pushed
        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]

        if curr_data is None:
            curr_viewed = 0
        else:
            curr_viewed = curr_data[0]

        if curr_viewed == how_many_available - 1:
            previous_disabled = False
            next_disabled = True
        elif curr_viewed == 0:
            previous_disabled = True
            next_disabled = False
        else:
            previous_disabled = False
            next_disabled = False

        return previous_disabled, next_disabled

    @dash_app.callback(Output("dropdown_mushroom_option", "options"),
                       Input('mushrooms_viewer_data', 'data'))
    def dropdown_options(data):
        if data is None:
            return [{'label': None, "value": None}]

        available_mushrooms = [{'label': x[1]['MushroomNameInFormal'], 'value': x[0]} for x in enumerate(data)]

        return available_mushrooms

    @dash_app.callback([Output("mushroom_informal_name_view", "children"),
                        Output("mushroom_formal_name_view", "children"),
                        Output("mushroom_info", "children")],
                       Input('mushrooms_viewer_current_view', 'data'))
    def card_view(data):
        if data is None:
            return None

        position, data = data

        formal_name = data['MushroomNameFormal']
        informal_name = data['MushroomNameInFormal']
        info = []
        for x, y in data['MushroomInfo'].items():
            info.append(html.H1(x, className='card-title'))
            info.append(html.Hr(className="my-1"))
            info.append(html.H4(y, className='card-title'))

        return [informal_name], formal_name, info

    @dash_app.callback(Output("mushroom_toxic_badge", "children"),
                       Input('mushrooms_viewer_current_view', 'data'))
    def card_view_name(data):
        if data is None:
            return None

        position, data = data

        if data is None:
            return 'primary'

        if data['Toxic']:
            badge = dbc.Badge('Trujący!', color='danger')
        else:
            badge = dbc.Badge('Jadalny', color='success')

        return badge

    @dash_app.callback(Output("mushroom-card", "color"),
                       Input('mushrooms_viewer_current_view', 'data'))
    def card_toxic_marker(data):
        if data is None:
            return 'primary'

        if data[1]['Toxic']:
            return 'danger'

        return 'success'

    @dash_app.callback(Output("curr_mushroom_imgs", "items"),
                       Input('mushrooms_viewer_current_view', 'data'))
    def imgs_view(data):
        if data is None:
            return None

        position, data = data

        imgs = [{'key': str(nr), 'src': x} for nr, x in enumerate(data['Photos'])]

        return imgs
