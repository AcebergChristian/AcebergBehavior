import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac


home_layout = html.Div(
    [
        fac.AntdSpace(
            [
                html.Div(
                    ["新闻"],
                    id='home-div_news',
                    style={"cursor":"pointer"}
                ),
                html.Div(["hao123"]),
                html.Div(["地图"])
            ],
            align="start",
            style={
                "fontSize": 14,
                "marginLeft": 40,
                "display": "flex",
                "gap": 20,
                "alignItems": "center",
                "width": "100%",
                "height": 32,
                "backgroundColor": "#0a071c",
                "color": "#ffffff",
                "cursor":"pointer"
            },
        ),
        fac.AntdSpace(
            [
                fac.AntdImage(
                    src="https://www.baidu.com/img/PCfb_5bf082d29588c07f842ccde3f97243ea.png",
                    style={
                        "width": 240,
                    },
                    preview=False
                ),
                fac.AntdSpace(
                    [
                        fac.AntdInput(id="search", mode='search',style={"width": 400, }),
                    ]
                ),
                fac.AntdSpace(
                    [
                        html.Div(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H4(f"标题_{item}"),
                                        html.Div(
                                            "内容内容内容内容内容内容内容内容内容"
                                        ),        
                                        
                                    ]
                                )
                            for item in range(1, 8)
                            ],
                            id="newlist",
                            style={
                                "marginTop": 100,
                                "width": 500,
                                "height": 600,
                                "backgroundColor": "rgba(255,255,255,0.8)",
                            },
                        ),
                        html.Div(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H5("热搜榜 >"),
                                    ],
                                ),
                            ],
                            id="newrank",
                            style={
                                "marginTop": 100,
                                "width": 300,
                                "height": 600,
                                "backgroundColor": "rgba(255,255,255,0.8)",
                            },
                        ),
                    ]
                ),
            ],
            align="center",
            direction="vertical",
            style={"width": "100%", "height": "100%","overflowY":"scroll" },
        ),
    ],
    style={
        "width": "100%",
        "height": "100vh",
        "backgroundImage": "url('https://dss3.bdstatic.com/iPoZeXSm1A5BphGlnYG/skin/54.jpg')",
        "overflowY":"hidden"  
    },
)

