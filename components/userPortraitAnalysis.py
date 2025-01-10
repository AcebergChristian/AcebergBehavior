import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


staticdata = [
    {
        "title": "总用户数",
        "value": "2888",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {
        "title": "在线用户数",
        "value": "2000",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {
        "title": "离线用户数",
        "value": "888",
        "time": "2024-08-08",
        "qoq": 30,
        "yoy": -20,
    },
    {"title": "注销用户数", "value": "88", "time": "2024-08-08", "qoq": 30, "yoy": -20},
]

userPortraitAnalysis_layout = html.Div(
    [
        # 指标统计
        html.Div(
            [       
                    fac.AntdTag(
                        content="总用户数",
                        color="blue",
                        bordered=False,
                        style={
                            "fontSize": "14px",
                        }
                    ),
                    fac.AntdText(
                        id="userPortraitAnalysis_totalusernum",
                        style={
                            "color": "#292d36"},
                    ),
                    
                    fac.AntdTag(
                        content="画像目标人群",
                        color="geekblue",
                        bordered=False,
                        style={
                            "fontSize": "14px",
                        }
                    ),
                    fac.AntdText(
                        id="userPortraitAnalysis_targetusernum",
                        style={
                            "color": "#8492a6"}
                    ),
                    
                    fac.AntdTag(
                        content="占全部用户",
                        color="green",
                        bordered=False,
                        style={
                            "fontSize": "14px",
                        }
                    ),
                    fac.AntdText(
                        id="userPortraitAnalysis_targetpercent",
                        style={
                            "color": "#475669",
                            "fontWeight": "bold",
                        },
                    ),
            ],
            id="userPortraitAnalysis_indi",
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "flex-start",
                "alignItems": "center",
                "gap": 12,
                "margin": "0 0 10px 0",
                "padding": "0 0 0 20px",
                "width": "100%",
                "height": "50px",
                "backgroundColor": "#fff",
                "borderRadius": 6,
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
            },
        ),
        
        
        
        # 搜索区域
        html.Div(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="userPortrait-user_meet",
                                    placeholder="用户满足",
                                    allowClear=True,
                                    style={
                                        "width": 220,
                                    },
                                ), label='用户满足'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id="userPortrait-user_meet_input",
                                    placeholder="用户满足关键字",
                                    allowClear=True,
                                    style={
                                        "width": 180,
                                    },
                                ), label=''
                            ),
                            
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px",
                        }),
                    fac.AntdRow([         
                        fac.AntdFormItem(
                            fac.AntdDateRangePicker(
                                id="userPortrait-datetimerange",
                                placeholder=['开始日期时间', '结束日期时间'],
                                showTime=True,
                                needConfirm=True,
                                style={
                                    "width": 220,
                                }
                            ), label='时间范围'
                        ),
                        fac.AntdFormItem(
                                    fac.AntdButton(
                                        '重置',
                                        id="userPortraitAnalysis-reset",
                                        type='dashed'),
                                    wrapperCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '搜索',
                                        id="userPortraitAnalysis-search",
                                        type='primary'
                                    ),
                                    wrapperCol={'offset': 4},
                                )
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px",
                        }
                        ),
                        
                        
                        
                    ],
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                    style={
                        'width': "100%",
                        "margin": "10px 10px",
                    },
                ),
            ],
            id="userPortraitAnalysis_searchArea",
            style={
                "display": "flex",
                "justifyContent": "flex-start",
                "gap": "10px",
                "width": "100%",
                "height": "150px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
                "overflowY": "auto",
            },
        ),
        

        html.Div(
            [
                # 年龄chart
                html.Div(
                    id="userPortraitAnalysis_chart_age",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
                # 性别chart
                html.Div(
                    id="userPortraitAnalysis_chart_sex",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
                # os chart
                html.Div(
                    id="userPortraitAnalysis_chart_os",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
                # 地域chart
                html.Div(
                    id="userPortraitAnalysis_chart_loc",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
                # apprun chart
                html.Div(
                    id="userPortraitAnalysis_chart_apprun",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
                # pay chart
                html.Div(
                    id="userPortraitAnalysis_chart_pay",
                    style={
                        "width": "49%",
                        "height": 300,
                        "borderRadius": 6,
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    },
                ),
            ],
            id="userPortraitAnalysis_charts",
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center",
                "gap": 10,
                "margin": "10px 0",
                "width": "100%"
            },
        ),
        
        
        


    ]
)
