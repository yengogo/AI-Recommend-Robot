import dash_bootstrap_components as dbc
from dash import dcc, html

colors = ["warning", "danger", "info", "secondary", "primary", "success"]


def Card(imgUrl, title, groupid, price, tags, idx, ids):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            dbc.CardImg(
                                src=imgUrl,
                                className="img-fluid rounded-start",
                            ),
                            html.Div(
                                groupid,
                                className="card-text text-center mt-2 mb-2",
                                style={'font-weight': 'bold',
                                       'font-size': 18,
                                       'color': '#744327',
                                       'font-family': 'PingFang',
                                       'background-color': '#e0c095'}
                            ),
                            html.Div(
                                price,
                                className="card-text text-center",
                                style={'font-weight': 'bold',
                                       'font-size': 18,
                                       'color': '#744327',
                                       'font-family': 'PingFang',
                                       'background-color': '#e0c095'}
                            )],
                        className="col-md-4 p-2 ",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(
                                    title,
                                    className="card-title text-left text-sm-start",
                                    style={
                                        'font-weight': 'bold',
                                        'font-family': 'PingFang',
                                        # 'color': '#35454c',
                                        'font-size': 20,
                                        'color': '#744327',
                                    }),
                                html.Div(
                                    [dbc.Badge(tag, color=colors[i], className="me-1")
                                     for i, tag in enumerate(tags)],

                                    style={'display': 'flex',
                                           'flex-wrap': 'wrap',
                                           'gap': '7px',
                                           'color': 'black',
                                           'font-family': 'PingFang',
                                           'font-size': 18
                                           },
                                ),
                            ]
                        ),
                        className="col-md-6 ",
                    ),
                    dbc.Col(
                        # dbc.CardLink("GO!", href=prod_url), className="col-md-2"
                        # dbc.Button("GO!", href=prod_url,
                        #            external_link=True, color="primary"),
                        [
                            dbc.Button(
                                "GO!", id=f"open-fs{idx}", color="primary"
                            ),
                            dbc.Spinner(html.Div(id=f"loading-{idx}")),
                        ],
                        className="col-md-2 75vh",
                        style={
                            'textAlign': 'center',
                        },
                    )
                ],
                className="g-0 d-flex align-items-center",
            ),
            # html.Div(dcc.Textarea(
            #     id=f"test-op{idx}",
            #     value=str(idx),
            #     # style={"visibility": "hidden"}
            # )),
            html.Div([
                # dcc.Textarea(
                #     id=f"tmp{idx}",
                #     value=str(idx),
                #     style={"visibility": "hidden"}
                # ),
                # dbc.Button("Open modal", id="open_test", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalHeader(close_button=True),
                        dbc.ModalBody(
                            id=f"md_body{idx}",
                            style={
                                'font-weight': 'bold',
                                'font-size': 18,
                                'color': '#744327',
                                # 'font-family': 'DFKai-sb',
                                'background-color': 'rgb(228, 212, 196)'}
                        ),
                    ],
                    id=f"modal-fs{idx}",
                    is_open=False,
                    size="xl",
                    # fullscreen=True
                ),
            ]),
        ],
        className="mb-3 mt-2 ",
        style={
            "maxWidth": "540px",
            "maxHeight": "500px",
            #    'flex-wrap': 'wrap',
            #    "height": "100px",
                'border': '5px solid rgb(190, 190, 190)',
            'background': '#e4d4c4',
            'borderRadius': '20px'
        },
        id=f'card{ids}'
    )
