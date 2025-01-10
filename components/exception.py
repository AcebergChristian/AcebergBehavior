import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes



exception_layout = html.Div(
    [
        fac.AntdEmpty(
            image='/assets/images/exception.png',
            description=fac.AntdText('当前页面开发中...', type='secondary'),
            imageStyle={'height': 250},
        )
    ],
            id="exception_div",
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "width": "100%",
                "height": "94%",
                "borderRadius": 6,
                "padding": 8,
                "margin": "10px 0px 10px 0px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff"
            },
        )