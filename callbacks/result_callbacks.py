from dash import Input, Output, State, ctx, dcc, html, no_update
import json
import requests
import time
from models.rq_api import product_api
from config.basic import PROJECT_PATH
from views.result import final
from config import basic

with open(PROJECT_PATH + '/src/test.json', 'r', encoding='utf-8') as jsfile:
    card_data = json.load(jsfile)


def result_page(app):

    for idx in range(len(card_data)):
        @app.callback(
            [Output(f"modal-fs{idx}", "is_open"),
             Output(component_id=f'md_body{idx}',
             component_property='children')],
            Input(f"open-fs{idx}", "n_clicks"),
            [State("chat-photo1", "children"),
             State(f"card{idx}", "children"),
             State(f"modal-fs{idx}", "is_open")],
            prevent_initial_call=True
        )
        def toggle_modal(n1, photo, card, is_open):
            # print(photo)
            img_name = basic.PROJECT_PATH + "/" + photo['props']['src']
            group_id = card[0]['props']['children'][0]['props']['children'][1]['props']['children']
            # group_id = '21TSKHH001'
            prod_info = product_api(str(group_id))
            tour_id = prod_info['TOUR_ID']

            # if tour_id != '21TWIELA01':
            #     tour_id = '21TWIELA01'

            tmp_arr = card[0]['props']['children'][1]['props']['children']['props']['children'][1]['props']['children']

            tour_tag_list = [i['props']['children'] for i in tmp_arr]

            url = 'http://10.35.2.42/api/pic/files'

            data = {"group_id": tour_id}
            with open(img_name, "rb") as f:
                files = {"file": f}
                response = requests.post(url, files=files, data=data)
                if response.status_code == 200:
                    print('虛擬人物成功合成影片')

            if n1:

                return not is_open, final(tour_id, tour_tag_list, prod_info)
            return is_open

        @app.callback(
            Output(f"loading-{idx}", "children"), [Input(f"open-fs{idx}", "n_clicks")]
        )
        def load_output(n):
            if n:
                time.sleep(3)
                return None
            return None

    @app.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
