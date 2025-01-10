import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


staticdata = [
    {
        "title": "总事件数",
        "value": "128",
        "time": "2024-08-08",
        "qoq": 8,
        "yoy": -8,
    },
    {
        "title": "已关联事件数",
        "value": "2000",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -29,
    },
    {
        "title": "未关联事件数",
        "value": "888",
        "time": "2024-08-08",
        "qoq": 40,
        "yoy": -22,
    },
    {
        "title": "停用事件数",
        "value": "88",
        "time": "2024-08-08",
        "qoq": 43,
        "yoy": -29
    },
]


funnelAnalysis_layout = html.Div(
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
            id="funnelAnalysis_indicator",
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
                fac.AntdSelect(
                    id="event_name_list",
                    placeholder="事件名称",
                    allowClear=True,
                    mode="multiple",
                    maxTagCount=3,
                    style={
                        "width": 360,
                    },
                ),
                fac.AntdDateRangePicker(
                    id="event_datetime",
                    placeholder=['开始日期时间', '结束日期时间'],
                    showTime=True,
                    needConfirm=True,
                ),
                fac.AntdButton(
                    "重置",
                    id="funnelAnalysis-reset",
                    type="dashed",
                ),
                fac.AntdButton(
                    "搜索",
                    id="funnelAnalysis-search",
                    type="primary",
                ),
            ],
            id="funnelAnalysis-searchbar",
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
        


        # 事件分组柱状图 折线图
        html.Div(
            id="funnelAnalysis_chart_funnel",
            style={
                "width": "100%",
                "height": "340px",
                "borderRadius": 6,
                "padding": 8,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
            },
        ),
        
        
        # 事件数据table
        html.Div(
            [   
                html.H4("表格展示",
                    style={
                        "margin": 8,
                    }
                ),
                fac.AntdTable(
                    id="funnelAnalysis_chart_funnelTable_table",
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
            id="funnelAnalysis_chart_funnelTable",
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
        
        
        
  
    ]
)
