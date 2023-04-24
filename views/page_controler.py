from __future__ import annotations
from dash import Dash, dcc, html
import json
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
from utils.general import Layout
from views.card import Card
from views.chatbot import Chat_Container
from config.basic import PROJECT_PATH
import json
import requests

layout = Layout()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

with open(PROJECT_PATH + '/src/test.json', 'r', encoding='utf-8') as jsfile:
    card_data = json.load(jsfile)

prod_url = "https://google.com"


def upload_component():
    return [
        html.Div(id='output-image-upload', className="d-flex  m-5 flex-wrap align-content-start",
                 style={'height': '75vh',
                        'border': '10px solid rgb(190, 190, 190)'

                        }),

        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '60%',
                'height': '50px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                # "marginTop": "10px",
                "marginLeft": "180px",
                "backgroundColor": 'white'
            },
            # Allow multiple files to be uploaded
            multiple=True
        )
    ]


def tour_guide_component():
    return [
        Chat_Container(),
    ]

# 初始值


def card_list_component():

    hresult = requests.get(
        url='http://10.35.2.42/api/pic/hot_popular?prompt=hot')
    cardlist_templete = [Card(imgUrl=i['img_url'], title=i["prod_name"], groupid=i['tour_id'],
                              price='$'+str(i['prod_price']), tags=i['labels'],idx=i,ids=i) for i in hresult.json()]
    return html.Div(
        children=[
            html.Div(
                children=[
                    dbc.Button("Popular!", n_clicks=0, color="warning", id='popular-button',
                               style={'width': '20%'},  className="me-2"),
                    dbc.Button("Hot!", n_clicks=0, color="danger", id='hot-button',
                               style={'width': '20%'}),
                ],
                className="d-flex w-100",
                id="hot-popular-buttons"
            ),
            html.Div(
                children=[*cardlist_templete],
                id='card-component'
            )
        ])



def updload_view():
    components = [

        # {"md": 8, "content": upload_component()},
        {"md": 8, "content": tour_guide_component()},
        {"md": 4, "content": card_list_component(),
         "className": "vh-100 overflow-auto"}
    ]

    return html.Div(
        # layout.row(imgrow),
        layout.row(components),

        # className="d-flex justify-content-center align-items-center",
        style={
            'backgroundImage': 'url(assets/example_pic/travel4.jpg)',
            'backgroundSize': 'contain'}


    )
