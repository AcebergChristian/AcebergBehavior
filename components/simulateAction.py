import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac


simulateAction_layout = html.Div(
    [
        html.Div(id="simulateAction-message"),
        html.Div(
            [
                fac.AntdButton(
                    id="simulateAction-autorun",
                    children="自动运行",
                    type="primary",
                ),
                fac.AntdInputNumber(
                    id="simulateAction-times",
                    style={"height": "32px"},
                ),
            ],
            id="simulateAction-bar",
            style={
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "center",
                "gap": 20,
                "width": "100%",
                "height": 50,
            },
        ),
        # simulateAction 容器div
        html.Div(
            [],
            id="simulateAction-container",
            style={
                "display": "flex",
                "flexDirection": "row",
                "flexWrap": "wrap",
                "justifyContent": "flex-start",
                "alignItems": "flex-start",
                "gap": 12,
            },
        ),
    ],
    style={
        "background-color": "#ffffff",
        "width": "100%",
        "height": "100%",
        "borderRadius": 10,
    },
)
