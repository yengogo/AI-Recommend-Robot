from dash import Dash, Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc
import inspect


class Layout():
    """
    A class to Layout

    Methods
    -------
    html()
        渲染html division 區塊, Row with columns
    Row()
        渲染Row 區塊,  with columns
    """
    colParams = inspect.getargspec(dbc.Col).args

    @staticmethod
    def html(data=list):
        cols = []
        for obj in data:
            params = {k: obj[k] for k in (obj.keys() & Layout.colParams)}
            col_value = dbc.Col(obj['content'], **params)
            cols.append(col_value)

        return html.Div([
            dbc.Row(cols)
        ])

    @staticmethod
    def row(data=list):
        cols = []
        for obj in data:
            params = {k: obj[k] for k in (obj.keys() & Layout.colParams)}
            col_value = dbc.Col(obj['content'], **params)
            cols.append(col_value)

        return dbc.Row(cols, className="w-100")
