import dash
import pathlib
# import dash_daq as daq
from dash import html, dcc, callback
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from views.page_controler import updload_view
from views.result import final
# from callbacks.img_upload_callback import upload_image
from views.chatbot import Chat_Container
from callbacks.dropdown_callbacks import tour_main_callbacks
from callbacks.chatroom_callback import chatroom_flow
from callbacks.result_callbacks import result_page
from datetime import datetime, date, timedelta

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=['bootstrap.min.css', dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,
                          'https://fonts.googleapis.com/css?family=Noto+Sans+TC'],
    suppress_callback_exceptions=True,
    # server=server
)
server = app.server
app.title = "HACKTHON"
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# upload_image(app)

tour_main_callbacks(app)
chatroom_flow(app)
result_page(app)

app.layout = html.Div(
    id="app-container",
    children=[
        updload_view(),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=55688, host="0.0.0.0")
