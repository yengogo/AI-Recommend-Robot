from utils.general import Layout
from dash import Input, Output,html
import dash_bootstrap_components as dbc
from models.rq_api import weather_api, product_api, similar_api
import time
import requests
import base64
import random
import json
from config.basic import PROJECT_PATH

layout = Layout()


def introduce(tour_tag_list, prod_info):
    # res = product_api(str(group_id))
    # if res['rDesc'] == "查無資料":
    #     res = product_api("2021TC0086")
    # tour_id = res['TOUR_ID']
    title = prod_info['TOUR_INSIDE_NAME']
    image = prod_info['IMAGEURL']

    group_info = prod_info['GROUP_INFO'][0]

    # title = '日本旅遊|2023富士山登山健行五日'
    # image = 'https://static.liontech.com.tw/cmspic/PIC2004-011398/M_PIC2004-011398.jpg'
    # tour_tag_list = ["親子", "美容", "電影院"]
    # group_info = {
    #     'SALE_CURR_ISO': 'TW',
    #     'B2C_LOW_PRICE': '10萬',
    # }

    tags = []
    tag_style = {"font-size": "1.1em","padding": "5px","margin": "2px"}
    for i in tour_tag_list:
        tags.append(dbc.Badge(i, color="secondary", className="me-1 float-right",style=tag_style))

    title_style = {
        'font-weight': 'bold',
        'font-size': "1.5em",
        'color': '#744327',
        'font-family': 'PingFang',
        'background-color': '#e0c095'
    }
    return dbc.Row(
        [
            dbc.Col(
                dbc.CardImg(src=image, top=True),
                className="col-md-6",
            ),
            dbc.Col(
                html.Div(
                    [
                        html.H4(title, className="card-title", style=title_style),
                        html.P("🎈", className="bday-decor bday-decor--top-right float"),
                        html.Div(tags),
                        html.Br(),
                        html.P([
                            html.B(group_info['SALE_CURR_ISO'], className="col-md-6"),
                            " : ",
                            html.B(group_info['B2C_LOW_PRICE'], style={"color": "red"}),
                        ],style={'background-color': '#e0c095', 'font-weight': 'bold', 'font-size': "1.3em"}),
                    ],
                    # className="card-block",
                    style={"margin-left": "10px"}
                ),
                className="col-md-6",
                align="start"
            ),
        ],
        className="g-0 d-flex align-items-center card-block",
    )


def video(tour_id=None):

    return html.Div(
        children=[
            html.Video(
                controls=True,
                id='movie_player',
                src=f"http://10.35.2.42/api/pic/video?grp_id={tour_id}",
                # src=f"http://10.35.2.42/api/video/product?grp_id={group_id}",
                # autoPlay=True,
                # style={"max-width": "100%", "height": "auto"}
                style={"width": "100%", "height": "auto"}
            ),
        ],
    )


def weather(tourid):
    # tourid = '21TSKHH001'
    with open(PROJECT_PATH + f'/src/tour_json_file/{tourid}.json', 'r', encoding='utf-8') as jsfile:
        json_data = json.load(jsfile)

    fake_data = []
    for json_day in json_data:
        tmp = []
        for poi in json_day:
            tmp.append({'Lng': poi['Lng'], 'Lat': poi['Lat'], 'poi': poi['Name']})
        fake_data.append(tmp)
    # print("127", fake_data)
    # fake_data = [
    #     {'citys': ['台北市','台中市','新竹縣']},
    #     {'citys': ['高雄市','桃園市']},
    # ]

    day_arr = []
    for i, day in enumerate(fake_data):
        city_arr = []
        for geo in day:
            api_data = weather_api(geo, i, tourid)
            # print(api_data)
            # MaxT = api_data['weather'][0]
            # MinT = api_data['weather'][1]
            # Wx = api_data['weather'][2]
            # Pop = api_data['weather'][3]
            # time.sleep(0.1)

            # maxT = MaxT['time'][i + 1]['elementValue'][0]['value']
            # minT = MinT['time'][i + 1]['elementValue'][0]['value']
            # wx = Wx['time'][i + 1]['elementValue'][0]['value']
            # pop = Pop['time'][i + 1]['elementValue'][0]['value']
            # location = api_data['location'][:3]
            maxT = api_data["weather"][0]
            minT = api_data["weather"][1]
            wx = api_data["weather"][2]
            pop = api_data["weather"][3]
            location = api_data['location']
            # maxT = "30"
            # minT = "20"
            # wx = random.choice(['雨','晴','no'])
            # pop = "20"
            print(wx)
            if '雨' in wx or 'rain' in wx:
                icon_type = 'bi bi-cloud-rain-heavy'
                background = 'rainy'
            elif '晴' in wx or 'sky' in wx:
                icon_type = 'bi bi-cloud-sun'
                background = 'sunny'
            else:
                icon_type = 'bi bi-clouds'
                background = 'partialy-cloudy'
            tmp = html.Section(
                [
                    html.Div(
                        [
                            html.Div(html.H2(className=icon_type), className="weatherIcon"),
                            html.Div(
                                [
                                    html.Div(html.P(f'第{i+1}天'), className="title"),
                                    html.Div(html.B(location), className="city"),
                                ]
                            )
                        ],
                        className="title__container"
                    ),
                    html.Div(
                        [
                            html.P(geo['poi'], style={"color":"gray"}),
                            html.Div(
                                [
                                    html.Div(html.P(str(maxT) + "ºC"), className="temperature__max"),
                                    html.Div(html.P(str(minT) + "ºC"), className="temperature__min"),
                                ],
                                className="temperature"
                            )
                        ],
                        className="main"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(html.B(" " + pop + "%",className="info__title"),className="bi bi-umbrella"),
                                    # html.H3(pop),
                                ],
                                className="visibility"
                            )
                        ],
                        className="info__container"
                    ),
                ],
                className=f"weatherCard {background}"
            )

            city_arr.append(tmp)

        day_arr.append(
            layout.row([{"width": {"size": 10, "offset": 1}, "content": html.Div(city_arr, className="container__inner")}])
        )

    return day_arr


def recommand_card(ele):

    img = requests.get(ele['img_url'])
    if img.status_code == 200:
        img = ele['img_url']
    else:
        img = 'https://uwww.liontravel.com/cto/view/default16-9.jpg'
    return dbc.Card(
        [
            dbc.CardImg(src=img, top=True, style={'height':'120px', 'width':'100%'}),
            dbc.CardBody(
                [
                    html.H4(ele['prod_name'], className="card-title", style= {'font-weight': 'bold',
                        'font-size': "1.1em",
                        'color': '#744327',
                        'font-family': 'PingFang'
                    }),
                    dbc.Button(
                        [
                            html.I(className="bi bi-currency-dollar"),
                            html.I("  "),
                            ele['prod_price'],
                        ],
                        href=ele['prod_url'],
                        external_link=True,
                        outline=True,
                        color="danger",
                        className="me-1"
                    ),
                    # html.P(ele['prod_price'], href=ele['prod_url'], external_link=True, className="card-text"),
                ]
            ),
        ],
        style={"margin":"2px"},
    )


def recommand(tour_id=None):
    # print(tour_id)
    arr1, arr2, arr3 = [],[],[]
    num = 4
    # similar_result = similar_api(tour_id)[:4]
    # print(similar_result)
    if tour_id:
        for i, ele in enumerate(similar_api(tour_id)[:4]):
            arr1.append({"md": int(12/num), "content": html.Div(recommand_card(ele))})

        for i, ele in enumerate(similar_api(tour_id)[4:8]):
            arr2.append({"md": int(12/num), "content": html.Div(recommand_card(ele))})

        for i, ele in enumerate(similar_api(tour_id)[8:]):
            arr3.append({"md": int(12/num), "content": html.Div(recommand_card(ele))})

        return [layout.row(arr1), layout.row(arr2), layout.row(arr3)]


def final(tour_id, tour_tag_list, prod_info):
    components_1 = [
        {"width": {"size": 10, "offset": 1}, "content": introduce(tour_tag_list, prod_info)},
    ]

    components_2 = [
        {"width": {"size": 10, "offset": 1}, "content": video(tour_id)},
    ]

    btn = dbc.Button(
        '查看天氣預報',
        id='collapse-button',
        # style={'width': '100%'},
        n_clicks=0,
        # outline=True,
        color="success",
        size="lg",
        className="d-grid gap-2 col-6 mx-auto"
    )

    data = [
        html.Br(),
        layout.row(components_1),
        html.Br(),
        layout.row(components_2),
        html.Br(),
        layout.row([{"width": {"size": 10, "offset": 1}, "content": html.Div(btn)}]),
        dbc.Collapse(
            weather(tour_id),
            id="collapse",
            is_open=False,
        ),
        html.Br(),
        # recommand(tour_id),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    recommand(tour_id)[0], title="第1頁", style={'background-color': 'rgb(228, 212, 196)'}
                ),
                dbc.AccordionItem(
                    recommand(tour_id)[1], title="第2頁", style={'background-color': 'rgb(228, 212, 196)'}
                ),
                dbc.AccordionItem(
                    recommand(tour_id)[2], title="第3頁", style={'background-color': 'rgb(228, 212, 196)'}
                ),
            ],
            flush=True,
        ),
    ]
    # data.extend(weather())
    # print(weather())
    # components_3 = [
    #     {"width": {"size": 10, "offset": 1}, "content": weather()},
    # ]

    return html.Div(
        data,
        style={
            'border-color': 'white',
            'border-width': '10px',
            'border-style': 'dotted'
        }
    )
