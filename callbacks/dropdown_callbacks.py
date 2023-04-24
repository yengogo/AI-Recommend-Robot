import datetime
import base64
import pandas as pd
import dash_bootstrap_components as dbc
import views.chatbot as chatbot
from dash import Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate
import os
import requests
import base64
from io import BytesIO
from PIL import Image
import json
from opencc import OpenCC
import random
from config import basic 
import dash
from views.card import Card

UPLOAD_DIRECTORY = basic.PROJECT_PATH + '/assets'
cc = OpenCC('t2s')


def tour_main_callbacks(app):
    @app.callback(
        Output('tour-photo', 'children'),
        Output('home-tour-name', 'children'),
        Output('sex-dropdown', 'value'),
        Output('hair-dropdown', 'value'),
        Output('cloth-dropdown', 'value'),
        Output('pose-dropdown', 'value'),
        Output('background-dropdown', 'value'),
        Input('replace-image-button', 'n_clicks'),
        Input('next-button5', 'n_clicks'),
        State('sex-dropdown', 'value'),
        State('hair-dropdown', 'value'),
        State('cloth-dropdown', 'value'),
        State('pose-dropdown', 'value'),
        State('background-dropdown', 'value'),
        State('tour-photo', 'children'),
        prevent_initial_call=True
    )
    def update_output(n1, n2, sex, hair, cloth, pose, background, old_image):
        ctx = dash.callback_context
        tourguide_name = ''
        personailty = ''
        if sex == '女孩' or sex == '女人':
            tourguide_name = '獅芭菈汐'
            personailty = '可愛小女孩❤'
        else:
            tourguide_name = '獅芭樂希'
            personailty = '帥氣boy'

        if ctx.triggered_id == "replace-image-button":

            prompt_string = ''
            for item in [sex, hair, cloth, pose, background]:
                if item and isinstance(item, list):
                    join_word = ','.join(item)
                    prompt_string += join_word+','
                else:
                    prompt_string += str(item)+','

            prompt_string = '一個'+prompt_string[:-1]
            print(cc.convert(prompt_string))

            res_image = requests.get(
                f'http://10.35.2.42/api/pic/tourguide?prompt={cc.convert(prompt_string)}')

            numberlist = [i for i in range(10000000)]
            jpgname = f'tour_pic{str(random.choice(numberlist))}'
            print(jpgname)
            tour_pic = Image.open(BytesIO(res_image.content))
            tour_pic.save(
                basic.PROJECT_PATH + f'/assets/tour_pic/{jpgname}.jpg')

            if n1 is None:
                return old_image
            new_image = html.Img(src=f'assets/tour_pic/{jpgname}.jpg',
                                 style={'height': '200px', 'width': '200px'})

            print(sex)
            return [
                new_image,
                [
                    dbc.Input(
                        id="home-input1", value=tourguide_name, type="text", readonly=True, className="text-center"),
                    dbc.Input(
                        id="home-input2", value=personailty, type="text", readonly=True, className="text-center")
                ],
                sex,
                hair,
                cloth,
                pose,
                background,
            ]

        if ctx.triggered_id == "next-button5":
            return [
                html.Img(src=f'assets/example_pic/duck.jpg',
                         style={'height': '200px', 'width': '200px'}),
                html.Div([
                    dbc.Input(
                        id="home-input1", value=tourguide_name, type="text", readonly=True, className="text-center"),
                    dbc.Input(
                        id="home-input2", value=personailty, type="text", readonly=True, className="text-center"),
                ]),
                None,
                None,
                None,
                None,
                None,
            ]

    @app.callback(
        [
            Output('tourcard', 'className'),
            Output('chatroom', 'style'),
            Output('hot-popular-buttons', 'className'),
            Output('messagebox1', 'children'),
            Output('chat-photo1', 'children'),
            Output('chat-photo2', 'children'),
            Output('chat-photo3', 'children'),
            Output('chat-photo4', 'children'),
            Output('chat-photo5', 'children'),
        ],
        Input('hide-button', 'n_clicks'),
        Input('next-button5', 'n_clicks'),
        State('sex-dropdown', 'value'),
        State('tour-photo', 'children'),
        prevent_initial_call=True
    )
    def hide(n1, n2, sex, photo):
        ctx = dash.callback_context
        if ctx.triggered_id == "hide-button":
            next_page_text = ''
            if sex == '女孩' or sex == '女人':
                next_page_text = '獅芭菈汐'
            else:
                next_page_text = '獅芭樂希'

            photo['props']['style'] = {"width": "100px", "height": "6rem"}

            # if n1 is None:
            #     return {'display': 'block'}

            return [
                "d-none",
                {'display': 'block'},
                "d-none",
                dbc.Input(
                    id=f"input-1", value=f"你好呀我是{next_page_text}爹斯,請上傳1~5張圖片❤❤❤❤", type="text", readonly=True,
                    className="text-center",
                    style={'font-weight': 'bold',
                           'font-size': 20,
                           'color': '#744327',
                           'font-family': 'DFKai-sb',
                           'background-color': '#e4d4c4'}),
                photo,
                photo,
                photo,
                photo,
                photo,
            ]
        if ctx.triggered_id == "next-button5":
            return [
                "d-flex justify-content-center align-items-center w-100 h-100",
                {'display': 'none'},
                "d-block",
                None,
                None,
                None,
                None,
                None,
                None,
            ]
