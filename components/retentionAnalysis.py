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


retentionAnalysis_layout = html.Div(
    [
        
        # 搜索区域
        html.Div(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow([
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="first_event",
                                    placeholder="初始行为",
                                    allowClear=True,
                                    maxTagCount=3,
                                    style={
                                        "width": 220,
                                    },
                                ), label='初始行为'
                            ),
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="second_event",
                                    placeholder="后续行为",
                                    allowClear=True,
                                    maxTagCount=3,
                                    style={
                                        "width": 220,
                                    },
                                ), label='后续行为'
                            ),
                            fac.AntdFormItem(
                                fac.AntdSelect(
                                    id="other_event",
                                    placeholder="其他行为",
                                    mode="multiple",
                                    allowClear=True,
                                    maxTagCount=2,
                                    style={
                                        "width": 260,
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
                            fac.AntdSelect(
                                id="user_filter",
                                placeholder="用户筛选",
                                allowClear=True,
                                style={
                                    "width": 220,
                                },
                            ), label='用户筛选'
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id="user_filter_input",
                                placeholder="用户筛选关键字",
                                allowClear=True,
                                style={
                                    "width": 180,
                                },
                            ), label=''
                        ),
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
                                        id="retentionAnalysis-reset",
                                        type='dashed'),
                                    wrapperCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '搜索',
                                        id="retentionAnalysis-search",
                                        type='primary'
                                    ),
                                    wrapperCol={'offset': 4},
                                ),
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
                        #                 id="retentionAnalysis-reset",
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
            id="retentionAnalysis_searchArea",
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
        


        # 事件分组柱状图 折线图
        # html.Div(
        #     id="retentionAnalysis_chart_funnel",
        #     style={
        #         "width": "100%",
        #         "height": "340px",
        #         "borderRadius": 6,
        #         "padding": 8,
        #         "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
        #         "background": "#ffffff",
        #     },
        # ),
        
        
        # 事件数据table
        html.Div(
            [   
                html.H4("表格展示",
                    style={
                        "margin": 8,
                    }
                ),
                fac.AntdTable(
                    id="retentionAnalysis_table_table",
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
            id="retentionAnalysis_table",
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
        
        
        

        
        
  
    ],
    # style={
    #     "display": "flex",
    #     "flexDirection": "column"
    # }
)
