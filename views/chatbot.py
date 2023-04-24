from __future__ import annotations
from dash import Dash, dcc, html
import json
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
from config.basic import PROJECT_PATH
from utils.general import Layout
import json


layout = Layout()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

with open(PROJECT_PATH + '/src/test.json', 'r', encoding='utf-8') as jsfile:
    card_data = json.load(jsfile)


def Tour_Guide_Selector():
    return html.Div(
        dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            children=[

                                html.Div(
                                    dbc.CardImg(
                                        src='assets/example_pic/duck.jpg',
                                        className="img-fluid rounded-start",
                                        style={'width': '200px',
                                               'height': '200px'},

                                    ),
                                    className="p-3", id='tour-photo'
                                ),
                                html.Div(
                                    children=[
                                        dbc.Input(
                                            id="home-input1", value="獅芭菈夕", type="text", readonly=True, className="text-center",
                                            style={'font-weight': 'bold',
                                                   'font-size': 20,
                                                   'color': '#744327',
                                                   'font-family': 'DFKai-sb',
                                                   'background-color': '#e0c095'}),
                                        dbc.Input(
                                            id="home-input2", value="個性", type="text", readonly=True, className="text-center",
                                            style={'font-weight': 'bold',
                                                   'font-size': 20,
                                                   'color': '#744327',
                                                   'font-family': 'DFKai-sb',
                                                   'background-color': '#e0c095'}),
                                    ],
                                    className="d-flex flex-column align-items-center justify-content-center h-50 p-3",
                                    id='home-tour-name'
                                ),
                            ],
                            md=4
                        ),
                        dbc.Col([
                            html.Div(
                                children=[
                                    dcc.Dropdown(
                                        ['男孩', '男人', '女孩', '女人'], searchable=False, placeholder="性別與年齡",
                                        clearable=False, id='sex-dropdown', style={'width': '70%'}),
                                    dcc.Dropdown(
                                        ['金髮', '黑髮', '棕髮', '長髮', '短髮', '藍眼',
                                            '黑眼', '棕眼', '白皙皮肤', '可愛', '成熟'],
                                        searchable=False, placeholder="外觀", clearable=False, multi=True,
                                        id='hair-dropdown', style={'width': '70%'}),
                                    dcc.Dropdown(
                                        ['學生制服', '泳裝', '圍巾', '毛帽', 'T恤', '棒球帽'], searchable=False, multi=True, placeholder="服裝造型",
                                        clearable=False, id='cloth-dropdown', style={'width': '70%'}),
                                    dcc.Dropdown(
                                        ['上半身', '看向閱圖者', '全身', '微笑', '開心'], searchable=False, multi=True, placeholder="姿勢",
                                        clearable=False, id='pose-dropdown', style={'width': '70%'}),
                                    dcc.Dropdown(
                                        ['簡單背景'], searchable=False, multi=True, placeholder="背景",
                                        clearable=False, id='background-dropdown', style={'width': '70%'}),

                                ], id='dd-output-container',
                                className="d-flex flex-wrap pt-3 h-50 align-content-start overflow-auto"
                            ),

                            html.Div(
                                children=[
                                    dbc.Button("產生", n_clicks=0, color="danger",
                                               id='replace-image-button', style={'width': '40%'}),
                                    dbc.Button("確認!", n_clicks=0, color="success",
                                               id='hide-button', style={'width': '40%'}),
                                ],
                                className="d-flex justify-content-around align-items-center h-50"
                            )
                        ],
                            md=8
                        )
                    ],
                    className='h-100'
                    # className="g-0 d-flex align-items-center",
                )
            ],
            # className="mb-3 mt-2",
            id='testcard',
            style={"width": "800px",
                   "height": "500px",
                   'border': '10px solid rgb(190, 190, 190)',
                   'background-color': '#e4d4c4'
                   }
        ),
        id='tourcard',
        className="d-flex justify-content-center align-items-center w-100 h-100"
    )


def Chat_Item(number):
    def first_row_button_group():
        return html.Div([
            dcc.Upload(dbc.Button('CV-INPUT!', color='primary'),
                       multiple=True, id=f'cv-up-button'),
            # dcc.Upload(dbc.Button('NLP-INPUT!', color='warning'),
            #            multiple=True, id=f'nlp-up-button'),
        ], className='d-flex justify-content-end gap-3')

    def other_row_button_group():
        return html.Div([
            dbc.Button("按!", n_clicks=0, color="danger",
                       id=f'next-button{number}', style={'width': '50%'})
        ], className='d-flex  justify-content-end')

    return dbc.Row(
        children=[
            dbc.Col(
                dbc.CardImg(
                    src="assets/example_pic/duck.jpg",
                    className="img-fluid rounded-start",
                    style={
                        "width": "100px",
                        "height": "6rem",
                    },
                ),
                md=2,
                className="photo",
                id=f'chat-photo{number}'

            ),
            dbc.Col(

                dbc.Spinner(
                    html.Div(
                        children=[],
                        id=f'messagebox{number}',
                        className="d-flex align-items-center h-100"
                    ),

                ),
                className="message d-flex flex-column justify-content-center flex-1 h-100",
            ),
            dbc.Col(

                first_row_button_group() if number == 1 else other_row_button_group(),
                md=2,
                className="upload mt-4 ml-3",
                id=f'chat-button{number}'
            )
        ],
        id=f'chat-row{number}',
        className="d-flex mb-3 w-100",
        style={
            "height": "6rem",
            "border": "1px solid yellow",
        }
    )


def Chat_Item_List():
    return html.Div(
        children=[Chat_Item(i) for i in [1, 2, 3, 4, 5]],
        className="p-3 w-100 h-150 overflow-auto",
        style={
            "border": "1px solid blue",
            'display': 'none'
        }, id='chatroom'
    )


def Chat_Container():
    return html.Div(
        children=[
            Chat_Item_List(),
            Tour_Guide_Selector()
        ],
        style={
            "width": "100%",
            "height": "60%",
            # "border": "1px solid red"
        }
    )
