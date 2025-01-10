import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


staticdata = [
    {
        "title": "总用户数",
        "value": "3891",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {
        "title": "在线用户数",
        "value": "2198",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {
        "title": "离线用户数",
        "value": "1693",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {"title": "注销用户数", "value": "88", "time": "2024-08-08", "qoq": 30, "yoy": -20},
]

userData_layout = html.Div(
    [
        # html.Div(
        #     [
        #         html.H4("用户数据筛选"),
        #         fac.AntdSelect(
        #             options=[
        #                 {"label": "总用户数", "value": "total_usernum"},
        #                 {"label": "在线用户数", "value": "online_usernum"},
        #                 {"label": "离线用户数", "value": "offline_usernum"},
        #                 {"label": "注销用户数", "value": "logout_usernum"},
        #             ],
        #             defaultValue="total_usernum",
        #             style={"width": 120},
        #         ),
        #         fac.AntdInput(
        #             style={
        #                 "width": 300,
        #             }
        #         ),
        #     ],
        #     id="userData-search",
        #     style={
        #         "display": "flex",
        #         "flexDirection": "row",
        #         "justifyContent": "flex-start",
        #         "alignItems": "center",
        #         "gap": 20,
        #         "margin": "10px 0px 10px 0px",
        #         "width": "100%",
        #         "height": "32px",
        #     },
        # ),
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
                                        "color": "#8492a6",
                                    },
                                ),
                                fac.AntdIcon(
                                    icon=(
                                        "antd-caret-up"
                                        if item["qoq"] >= 0
                                        else "antd-caret-down"
                                    ),
                                    style={
                                        "fontSize": 14,
                                        "color": (
                                            "#38c994" if item["qoq"] >= 0 else "#fa6975"
                                        ),
                                    },
                                ),
                                fac.AntdText(
                                    f"{item['qoq']}%",
                                    style={
                                        "fontSize": 12,
                                        "color": (
                                            "#38c994" if item["qoq"] >= 0 else "#fa6975"
                                        ),
                                    },
                                ),
                                fac.AntdText(
                                    "同比: ",
                                    style={
                                        "marginLeft": 20,
                                        "fontSize": 12,
                                        "color": "#8492a6",
                                    },
                                ),
                                fac.AntdIcon(
                                    icon=(
                                        "antd-caret-up"
                                        if item["yoy"] >= 0
                                        else "antd-caret-down"
                                    ),
                                    style={
                                        "fontSize": 14,
                                        "color": (
                                            "#38c994" if item["yoy"] >= 0 else "#fa6975"
                                        ),
                                    },
                                ),
                                fac.AntdText(
                                    f"{item['yoy']}%",
                                    style={
                                        "fontSize": 12,
                                        "color": (
                                            "#38c994" if item["yoy"] >= 0 else "#fa6975"
                                        ),
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
            id="userData_indicator",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "140px",
            },
        ),
        # 性别 和 来源占比图
        fac.AntdRow(
            [
                html.Div(
                    id="userData_chart_Genderpie",
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
                    id="userData_chart_Sourcepie",
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
            },
        ),
        # 年龄 和 vip
        fac.AntdRow(
            [
                html.Div(
                    id="userData_chart_Agecutline",
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
                    id="userData_chart_Vipline",
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
            },
        ),
        # 职业 和 OS
        fac.AntdRow(
            [
                html.Div(
                    id="userData_chart_Careerpie",
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
                    id="userData_chart_OSpie",
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
            },
        ),
        # 活跃度
        html.Div(
            id="userData_chart_Activityline",
            style={
                "width": "100%",
                "height": "320px",
                "borderRadius": 6,
                "padding": 8,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        # 积分table
        html.Div(
            [   
                html.H3("积分",
                    style={
                        "margin": 8,
                    }
                ),
                fac.AntdTable(
                    id="userData_chart_Pointstable_table",
                    # data=users_query(),
                    # columns=columns,
                    rowSelectionWidth=50,
                    bordered=True,
                    maxHeight=240,
                    # pagination=[],
                    mode="server-side",
                    style={
                        "width": "100%",
                        "paddingRight": "10px",
                    },
                ),
            ],
            id="userData_chart_Pointstable",
            style={
                "width": "100%",
                "height": "400px",
                "borderRadius": 6,
                "padding": 8,
                "margin":"10px 0",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        # 地图
        html.Div(
            id="userData_chart_UserGraph",
            style={
                "width": "100%",
                "height": "520px",
                "borderRadius": 6,
                "padding": 8,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
    ],
    # style={
    #     "display": "flex",
    #     "flexDirection": "column"
    # }
)
