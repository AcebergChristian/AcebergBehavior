import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


staticdata = [
    {
        "title": "总标签数",
        "value": "2888",
        "time": "2024-08-08",
        "qoq": 28,
        "yoy": -18,
    },
    {
        "title": "已关联标签数",
        "value": "2000",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -29,
    },
    {
        "title": "未关联标签数",
        "value": "888",
        "time": "2024-08-08",
        "qoq": 40,
        "yoy": -22,
    },
    {
        "title": "停用标签数",
        "value": "88",
        "time": "2024-08-08",
        "qoq": 43,
        "yoy": -29
    },
]


tagAnalysis_layout = html.Div(
    [
        
        # 指标卡
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
                    },
                )
                for item in staticdata
            ],
            id="tagAnalysis_indicator",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "140px",
            },
        ),
        
        
        
        # 搜索bar
        html.Div(
            [
                fac.AntdInput(
                    id="tag_name",
                    placeholder="请输入标签名称",
                    style={"width": "200px"},
                ),
                fac.AntdSelect(
                    id="tag_datatype",
                    options=[
                        {"label": "文本", "value": "string"},
                        {"label": "数字", "value": "num"},
                        {"label": "日期时间", "value": "datetime"},
                        {"label": "其他", "value": "other"},
                    ],
                    placeholder="数据类型",
                    style={"width": 200},
                ),
                fac.AntdSelect(
                    id="tag_createmethod",
                    options=[
                        {"label": "手动创建", "value": "手动创建"},
                        {"label": "自定义", "value": "custom"},
                    ],
                    placeholder="标签来源",
                    style={"width": 120},
                ),
                fac.AntdSelect(
                    id="tag_status",
                    options=[
                        {"label": "激活", "value": "active"},
                        {"label": "未激活", "value": "inactive"},
                    ],
                    placeholder="标签状态",
                    style={"width": 120},
                ),
                fac.AntdButton(
                    "搜索",
                    id="tagAnalysis-search",
                    type="primary",
                ),
            ],
            id="tagAnalysis-search",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": 20,
                "width": "100%",
                "height": "50px",
                "background": "#ffffff",
            },
        ),
        

        
        # 标签数据table
        html.Div(
            [   
                html.H3("标签数据",
                    style={
                        "margin": 8,
                    }
                ),
                fac.AntdTable(
                    id="tagAnalysis_chart_Tagtable_table",
                    # data=users_query(),
                    # columns=columns,
                    rowSelectionWidth=50,
                    bordered=True,
                    maxHeight=240,
                    pagination={
                        'current': 1,
                        'pageSize': 10,
                    },
                    mode="server-side",
                    style={
                        "width": "100%",
                        "paddingRight": "10px"
                    },
                ),
            ],
            id="tagAnalysis_chart_Tagtable",
            style={
                "width": "100%",
                "height": "400px",
                "borderRadius": 6,
                "padding": 8,
                "margin":"10px 0",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff"
            },
        ),
        
        
        
        
        
        # 标签分组group占比 和重点标签rank6覆盖人数 
        fac.AntdRow(
            [
                html.Div(
                    id="tagAnalysis_chart_Taggrouppie",
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
                    id="tagAnalysis_chart_Importanttagcoverbar",
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
                "scrollbarWidth": 0,
            },
        ),
        
        
        
        
        
    
            
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        # # 年龄 和 vip
        # fac.AntdRow(
        #     [
        #         html.Div(
        #             id="tagAnalysis_chart_Agecutline",
        #             style={
        #                 "width": "48%",
        #                 "height": "320px",
        #                 "borderRadius": 6,
        #                 "padding": 8,
        #                 "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #                 "background": "#ffffff",
        #             },
        #         ),
        #         html.Div(
        #             id="tagAnalysis_chart_Vipline",
        #             style={
        #                 "width": "48%",
        #                 "height": "320px",
        #                 "borderRadius": 6,
        #                 "padding": 8,
        #                 "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #                 "background": "#ffffff",
        #             },
        #         ),
        #     ],
        #     style={
        #         "display": "flex",
        #         "flexDirection": "row",
        #         "justifyContent": "space-between",
        #         "margin": "10px 0px 10px 0px",
        #         "width": "100%",
        #         "height": "340px",
        #     },
        # ),
        # # 职业 和 OS
        # fac.AntdRow(
        #     [
        #         html.Div(
        #             id="tagAnalysis_chart_Careerpie",
        #             style={
        #                 "width": "48%",
        #                 "height": "320px",
        #                 "borderRadius": 6,
        #                 "padding": 8,
        #                 "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #                 "background": "#ffffff",
        #             },
        #         ),
        #         html.Div(
        #             id="tagAnalysis_chart_OSpie",
        #             style={
        #                 "width": "48%",
        #                 "height": "320px",
        #                 "borderRadius": 6,
        #                 "padding": 8,
        #                 "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #                 "background": "#ffffff",
        #             },
        #         ),
        #     ],
        #     style={
        #         "display": "flex",
        #         "flexDirection": "row",
        #         "justifyContent": "space-between",
        #         "margin": "10px 0px 10px 0px",
        #         "width": "100%",
        #         "height": "340px",
        #     },
        # ),
        # # 活跃度
        # html.Div(
        #     id="tagAnalysis_chart_Activityline",
        #     style={
        #         "width": "100%",
        #         "height": "320px",
        #         "borderRadius": 6,
        #         "padding": 8,
        #         "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #         "background": "#ffffff",
        #     },
        # ),
        
        # # 地图
        # html.Div(
        #     id="tagAnalysis_chart_UserGraph",
        #     style={
        #         "width": "100%",
        #         "height": "520px",
        #         "borderRadius": 6,
        #         "padding": 8,
        #         "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #         "background": "#ffffff",
        #     },
        # ),
    ],
    # style={
    #     "display": "flex",
    #     "flexDirection": "column"
    # }
)
