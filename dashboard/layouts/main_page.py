import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

carousel_header = dbc.Carousel(
    items=[
        {"key": "1", "src": './static/mainpage/main_page_1.jpg'},
        {"key": "2", "src": './static/mainpage/main_page_2.jpg'},
        {"key": "3", "src": './static/mainpage/main_page_3.jpg'},
    ],
    className="carousel-fade",
    interval=4000,
    controls=True
)


main_page = dbc.Container([
    dbc.Row(dbc.Col(carousel_header, lg=8, xxl=8, md=12, sm=12, xs=12, width=12), className="g-0", justify='center'),
], fluid=True)

