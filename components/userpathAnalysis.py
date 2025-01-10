import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes




userpathAnalysis_layout = html.Div(
    [
        
        # 搜索区域
        html.Div(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="userpath-userpath_action",
                                    placeholder="事件选择",
                                    allowClear=True,
                                    mode="multiple",
                                    maxTagCount=2,
                                    style={
                                        "width": 220,
                                    },
                                ), label='事件选择'
                            ),
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="userpath-startend",
                                    placeholder="起始结束",
                                    allowClear=True,
                                    options=[
                                        {"label": "以起始", "value": "forstart"},
                                        {"label": "以结束", "value": "forend"},],
                                    style={
                                        "width": 160,
                                    },
                                ), label=''
                            ),
                            
                            
                            fac.AntdFormItem(
                                fac.AntdInputNumber(
                                    id="userpath-userpath_sessioninterval",
                                    placeholder="session间隔(分钟)",
                                    min=0,
                                    max=2000,
                                    style={
                                        "width": 140,
                                    },
                                ), label='session间隔',
                                style={
                                        "width": 360,
                                },
                            )
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px"
                        }),
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="userpath-user_meet",
                                    placeholder="用户满足",
                                    allowClear=True,
                                    style={
                                        "width": 220,
                                    },
                                ), label='用户满足'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id="userpath-user_meet_input",
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
                                id="userpath-datetimerange",
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
                                        id="userpathAnalysis-reset",
                                        type='dashed'),
                                    wrapperCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '搜索',
                                        id="userpathAnalysis-search",
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
            id="userpathAnalysis_searchArea",
            style={
                "display": "flex",
                "justifyContent": "flex-start",
                "gap": "18px",
                "width": "100%",
                "height": "220px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
                "overflowY": "auto",
            },
        ),
        


        
        # userpath事件数据chart
        html.Div(
            [
                html.Div(
                    id="userpathAnalysis_chart_sankey",
                    style={
                        "width": "100%",
                        "height": "600px",
                        "borderRadius": 6,
                        "padding": 8,
                        "margin": "10px 0px 10px 0px",
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff",
                    },
                )   
            ]
        )
        


    ]
)
