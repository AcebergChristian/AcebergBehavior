import dash
from dash import html
import feffery_antd_components as fac

staticdata = [
    {
        "title": "订单量",
        "value": "6824",
        "time": "2024-09-09",
        "qoq": 19,
        "yoy": 9,
    },
    {
        "title": "GMV",
        "value": "3101299",
        "time": "2024-08-08",
        "qoq": 32,
        "yoy": -29
    },
    {
        "title": "订单用户数",
        "value": "3439",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20
    },
    {
        "title": "平均客单价",
        "value": "901.80",
        "time": "2024-08-08",
        "qoq": 32,
        "yoy": -17
    },
]


dynamicsalesAnalysis_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        fac.AntdText(
                            f"{item['title']}",
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
            id="dynamicsalesAnalysis_indicator",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "140px",
            },
        ),
        # 取消订单line图
        html.Div(
            id="dynamicsalesAnalysis_chart_cancelorder",
            style={
                "width": "100%",
                "height": "280px",
                "borderRadius": 6,
                "padding": 8,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        
        # 近30天GMV
        html.Div(
            id="dynamicsalesAnalysis_chart_gmv30",
            style={
                "width": "48%",
                "height": "280px",
                "borderRadius": 6,
                "padding": 8,
                "margin": "10px 0px 0px 0px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        # gmv各端贡献
        html.Div(
            id="dynamicsalesAnalysis_chart_gmvcontribute",
            style={
                "width": "48%",
                "height": "280px",
                "borderRadius": 6,
                "padding": 8,
                "margin": "10px 0px 0px 0px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        
        # 近各类商品销售趋势
        html.Div(
            id="dynamicsalesAnalysis_chart_salestrend",
            style={
                "width": "48%",
                "height": "280px",
                "borderRadius": 6,
                "padding": 8,
                "margin": "10px 0px 0px 0px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        
        # 各商铺占比
        html.Div(
            id="dynamicsalesAnalysis_chart_shoprate",
            style={
                "width": "48%",
                "height": "280px",
                "borderRadius": 6,
                "padding": 8,
                "margin": "10px 0px 0px 0px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        
        
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "flexWrap": "wrap",
        "justifyContent": "space-between",
        "alignItems": "center",
    }
)




# html.Div(
#     [
#         # layout 全局的messages
#         html.Div(id="layout-message"),
#         fac.AntdCenter(
#             [
#                 fac.AntdEmpty(
#                     image='/assets/images/logo.png',
#                     description = html.H3('当前页面开发中...'),
#                     imageStyle={'height': 120},
#                 )
#             ],
#             style={"width": "100%", "height": "100%"},
#         ),
#     ],
#     style={"width": "100%", "height": "100%"},
# )
