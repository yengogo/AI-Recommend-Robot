import base64
import pandas as pd
import dash_bootstrap_components as dbc
import views.chatbot as chatbot
from dash import Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate
import requests
import base64
import json
import base64
from views.card import Card
import dash


def Cls_List(tag):
    return html.Div([
        dbc.Badge(tag, pill=True,
                    color="info", className="me-3",
                    style={'display': 'flex',
                           'flex-wrap': 'wrap',
                           'gap': '7px',
                           'color': 'black',
                           'font-family': 'PingFang',
                           'font-size': 18
                           })
    ])


text1 = '獅芭菈夕正在幫你正在計算結果唷❤🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🚂'
text2 = '您剛剛上傳圖片的分類為'
text3 = '計算結果GO!'
text4 = '您的推薦結果已呈現在右邊的列表中🦔，選擇好按下GO可以和我進入下一段冒險'
text5 = '透過下面的區塊可以快速的協助您找到理想的旅遊產品~'

api_result = {}


def chatroom_flow(app):

    @app.callback(
        [Output('messagebox2', 'children'),
         Output('next-button2', 'color')],
        [Input('cv-up-button', 'contents'),
         #  Input('nlp-up-button', 'contents'),
         Input('next-button5', 'n_clicks')],
        prevent_initial_call=True
    )
    def show_meg2(cvContents, n5):
        ctx = dash.callback_context
        if ctx.triggered_id == "cv-up-button":
            tag_list = []
            byte_list = []
            if cvContents:
                for idx, pic in enumerate(cvContents):
                    content_type, content_string = pic.split(',')
                    decoded_image = base64.b64decode(
                        content_string)  # picture_byte
                    byte_list.append(decoded_image)

                pic_files = [('files', (f'files{i}', byte_list[i]))
                             for i in range(len(byte_list))]

                res_string = requests.post(
                    url='http://10.35.2.42/api/pic/pic_cls', files=pic_files)
                api_result.update(res_string.json())
                print(api_result)

                for i in api_result['catgorylist']:
                    tag = i.replace(
                        '[', '').replace(']', '').replace('"', '')
                    find_dash_index = tag.rfind('-')
                    tag = tag[find_dash_index+1:]
                    tag_list.append(tag)

            return html.Div([
                dbc.Input(
                    id=f"input-40", value=text2, type="text", readonly=True, className="text-center",
                    style={
                        'width': '40%',
                        'font-weight': 'bold',
                        'font-size': 20,
                        'color': '#744327',
                        'font-family': 'DFKai-sb',
                        'background-color': '#e4d4c4'
                    }),
                html.Div(children=[Cls_List(tag_list[i]) for i in range(len(tag_list))],
                         className="me-2",
                         style={'display': 'flex',
                                'justify-content': 'space-between',
                                'height': '100%',
                                'font-size': 'x-large'})
            ],
                className="me-2 d-flex w-100 justify-content-center",
            ), 'success'

        if ctx.triggered_id == "next-button5":
            return [
                None,
                'danger'
            ]

    @app.callback(
        [Output('messagebox3', 'children'),
         Output('next-button3', 'color')],
        [Input('next-button2', 'n_clicks'),
         Input('next-button5', 'n_clicks')],
        prevent_initial_call=True
    )
    def show_meg3(button2, n5):
        ctx = dash.callback_context
        if ctx.triggered_id == 'next-button2':
            return dbc.Input(
                id=f"input-3", value=text3, type="text", readonly=True, className="text-center ",
                style={'font-weight': 'bold',
                       'font-size': 20,
                       'color': '#744327',
                       'font-family': 'DFKai-sb',
                       'background-color': '#e4d4c4'}
            ), 'success'

        if ctx.triggered_id == 'next-button5':
            return [
                None,
                'danger'
            ]

    @app.callback(
        [Output('messagebox4', 'children'),
         Output('next-button4', 'color'),
         Output('card-component', 'children')],
        [Input('next-button3', 'n_clicks'),
         Input('next-button5', 'n_clicks'),
         Input('popular-button', 'n_clicks'),
         Input('hot-button', 'n_clicks')
         ],
        prevent_initial_call=True
    )
    def show_meg4(button3, n5, pbutton, hbutton):
        ctx = dash.callback_context
        if ctx.triggered_id == 'next-button3':
            return dbc.Input(
                id=f"input-4", value=text4, type="text", readonly=True, className="text-center ",
                style={'font-weight': 'bold',
                       'font-size': 20,
                       'color': '#744327',
                       'font-family': 'DFKai-sb',
                       'background-color': '#e4d4c4'}
            ), 'success',\
                html.Div([
                    Card(imgUrl=item['img_url'], title=item["prod_name"], groupid=item['group_id'], price='$'+str(item['prod_price']), tags=item['labels'] , idx=idx, ids=idx) for idx, item in enumerate(api_result['recommendation'])
                ], id='card-component')
        if ctx.triggered_id == 'next-button5':
            return [
                None,
                'danger',
                html.Div([
                    Card(imgUrl=i['img_url'], title=i["prod_name"], groupid=i['group_id'], price='$'+str(i['prod_price']), tags=i['labels'], idx=i, ids=i) for i in api_result['recommendation']
                ], id='card-component')
            ]

        if ctx.triggered_id == 'popular-button':
            presult = requests.get(
                url='http://10.35.2.42/api/pic/hot_popular?prompt=popular')
            print(presult.json())
            return \
                None,\
                None,\
                html.Div([
                    Card(imgUrl=i['img_url'], title=i["prod_name"], groupid=i['tour_id'], price='$'+str(i['prod_price']), tags=i['labels'], idx=i, ids=i) for i in presult.json()
                ], id='card-component')
        if ctx.triggered_id == 'hot-button':
            hresult = requests.get(
                url='http://10.35.2.42/api/pic/hot_popular?prompt=hot')

            return \
                None,\
                None,\
                html.Div([
                    Card(imgUrl=i['img_url'], title=i["prod_name"], groupid=i['tour_id'], price='$'+str(i['prod_price']), tags=i['labels'], idx=i, ids=i) for i in hresult.json()
                ], id='card-component')

    @app.callback(
        [Output('messagebox5', 'children'),
         Output('next-button5', 'color'),
         Output('next-button5', 'children')],
        [Input('next-button4', 'n_clicks'),
         Input('next-button5', 'n_clicks')],
        prevent_initial_call=True
    )
    def show_meg5(button3, n5):
        ctx = dash.callback_context
        if ctx.triggered_id == 'next-button4':
            return dbc.Input(
                id=f"input-5", value=text5, type="text", readonly=True, className="text-center ",
                style={'font-weight': 'bold',
                       'font-size': 20,
                       'color': '#744327',
                       'font-family': 'DFKai-sb',
                       'background-color': '#e4d4c4'}
            ), 'success', '上一頁'

        if ctx.triggered_id == 'next-button5':
            return [
                None,
                'danger',
                '按!'
            ]
