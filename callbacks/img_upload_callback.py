from collections import Counter
import datetime
import base64
import pandas as pd
# import views.img_upload as parse_contents
# import views.pixnet_basic as pixnet_basic
# from config import mongo
from dash import Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate
import os
from config import basic
# from views import settings

UPLOAD_DIRECTORY = basic.PROJECT_PATH + '/assets'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def parse_contents(contents, filename, date):
    return html.Div([
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        # [html.Div(
        #     html.Img(src=i, width='20%', height='20%'),
        #     className="vh-75 w-100 d-flex"
        # ) for i in contents],
        html.Img(src=contents, width='100%', height='100%'),
        # html.Hr(),
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ], className="w-25 h-25")


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def upload_image(app):
    @app.callback(Output('output-image-upload', 'children'),
                  Input('upload-image', 'contents'),
                  State('upload-image', 'filename'),
                  State('upload-image', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            for name, data in zip(list_of_names, list_of_contents):
                save_file(name, data)
            return children
