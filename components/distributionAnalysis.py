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


distributionAnalysis_layout = html.Div(
    [
        
        # 搜索区域
        html.Div(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="user_action",
                                    placeholder="用户行为",
                                    allowClear=True,
                                    maxTagCount=3,
                                    style={
                                        "width": 220,
                                    },
                                ), label='用户行为'
                            ),
                            
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px",
                        }),
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="user_meet",
                                    placeholder="用户满足",
                                    allowClear=True,
                                    style={
                                        "width": 220,
                                    },
                                ), label='用户满足'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    id="user_meet_input",
                                    placeholder="用户满足关键字",
                                    allowClear=True,
                                    autoComplete="off",
                                    style={
                                        "width": 180,
                                    },
                                ), label=''
                            ),
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="other_action",
                                    placeholder="其他行为",
                                    allowClear=True,
                                    maxTagCount=2,
                                    style={
                                        "width": 300,
                                    },
                                ), label='其他行为'
                            )
                        ],
                        style={
                            "display": "flex",
                            "gap": "18px",
                        }),
                    fac.AntdRow([         
                        fac.AntdFormItem(
                            fac.AntdDateRangePicker(
                                id="datetimerange",
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
                                        id="distributionAnalysis-reset",
                                        type='dashed'),
                                    wrapperCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '搜索',
                                        id="distributionAnalysis-search",
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
                        # fac.AntdRow(
                        #     [
                        #         fac.AntdFormItem(
                        #             fac.AntdButton(
                        #                 '重置',
                        #                 id="distributionAnalysis-reset",
                        #                 type='dashed'),
                        #             wrapperCol={'offset': 4},
                        #         ),
                        #         fac.AntdFormItem(
                        #             fac.AntdButton('搜索', type='primary'),
                        #             wrapperCol={'offset': 4},
                        #         ),
                        #     ],
                        #     style={
                        #         "display": "flex",
                        #         "gap": "18px",
                        #     },
                        # ),
                        
                    ],
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                    style={
                        'width': "100%",
                        "margin": "24px 10px",
                    },
                ),
            ],
            id="distributionAnalysis_searchArea",
            style={
                "display": "flex",
                "justifyContent": "flex-start",
                "gap": "18px",
                "margin": "10px 0px 10px 0px",
                "width": "100%",
                "height": "220px",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff",
                "overflowY": "auto",
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
                    id="distributionAnalysis_table_table",
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
                    conditionalStyleFuncs={
                    'date': """
                        (record, index) => {
                            console.log(record,index)
                            return {
                                style: {
                                    background: '#def0ff'
                                }
                            };
                        }
                    """,
                    },
                ),
            ],
            id="distributionAnalysis_table",
            style={
                "width": "100%",
                "height": "420px",
                "borderRadius": 6,
                "padding": 8,
                "margin":"10px 0",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff"
            },
        ),
        
        
        
    ]
)
