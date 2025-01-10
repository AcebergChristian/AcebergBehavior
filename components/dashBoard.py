import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


staticdata = [
    {
        "title": "全站PV",
        "value": "8888",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {
        "title": "全站UV",
        "value": "888",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20
    },
    {
        "title": "新注册用户数",
        "value": "88",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20
    },
    {
        "title": "新访问用户数",
        "value": "8",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20
    },
]

home_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        fac.AntdText(
                            f"{item['title']} (人)",
                            style={"fontSize": 14, "color": "#292d36"},
                        ),
                        fac.AntdText(
                            item["time"], style={"fontSize": 12, "color": "#8492a6"}
                        ),
                        fac.AntdText(
                            item["value"],
                            style={
                                "fontSize": 32,
                                "color": "#475669",
                                "fontWeight": "bold",
                            },
                        ),
                        fac.AntdRow(
                            [   
                                fac.AntdText(
                                    "环比: ",
                                    style={
                                        # "marginLeft": 20,
                                        "fontSize": 12,
                                        "color": "#8492a6"
                                    },
                                ),
                                
                                fac.AntdIcon(
                                    icon="antd-caret-up" if item['qoq'] >= 0 else "antd-caret-down",
                                    style={
                                            'fontSize': 14,
                                            "color": "#38c994" if item['qoq'] >= 0 else "#fa6975",
                                    }),
                                fac.AntdText(
                                    f"{item['qoq']}%",
                                    style={
                                        "fontSize": 12,
                                        "color": "#38c994" if item['qoq'] >= 0 else "#fa6975",
                                    },
                                ),
                                fac.AntdText(
                                    "同比: ",
                                    style={
                                        "marginLeft": 20,
                                        "fontSize": 12,
                                        "color": "#8492a6"
                                    },
                                ),
                                
                                fac.AntdIcon(
                                    icon="antd-caret-up" if item['yoy'] >= 0 else "antd-caret-down",
                                    style={
                                            'fontSize': 14,
                                            "color": "#38c994" if item['yoy'] >= 0 else "#fa6975",
                                    }),
                                fac.AntdText(
                                    f"{item['yoy']}%",
                                    style={
                                        "fontSize": 12,
                                        "color": "#38c994" if item['yoy'] >= 0 else "#fa6975",
                                    },
                                ),
                            ]
                        ),
                        
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "flex-start",
                        "padding": "20px 0 0 20px",
                        "width": "calc(24% - 20px)",
                        "height": "calc(100% - 20px)",
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                        # "boxShadow": "0 1px 2px -2px #00000029, 0 3px 6px #0000001f, 0 5px 12px 4px #00000017",
                    },
                )
                for item in staticdata
            ],
            id="home_indicator",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "140px",
            },
        ),
        fac.AntdRow(
            [
                html.Div(
                    id="home_chart_PVline",
                    style={
                        "width": "48%",
                        "height": "320px",
                        "borderRadius": 6,
                        "padding": 8,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                    },
                ),
                html.Div(
                    id="home_chart_UVline",
                    style={
                        "width": "48%",
                        "height": "320px",
                        "borderRadius": 6,
                        "padding": 8,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "340px",
            }
        ),
        html.Div(
            id="home_chart_UserGraph",
            style={
                "width": "100%",
                "height": "520px",
                "borderRadius": 6,
                "padding": 8,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        fac.AntdRow(
            [
                html.Div(
                    id="home_chart_Genderpie",
                    style={
                        "width": "48%",
                        "height": "320px",
                        "borderRadius": 6,
                        "padding": 8,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                    },
                ),
                html.Div(
                    id="home_chart_Sourcepie",
                    style={
                        "width": "48%",
                        "height": "320px",
                        "borderRadius": 6,
                        "padding": 8,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "340px",
            }
        ),
    ],
    # style={
    #     "display": "flex",
    #     "flexDirection": "column"
    # }
)
