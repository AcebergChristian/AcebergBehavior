import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes




customAnalysis_layout = html.Div(
    [
        html.Div(id="customAnalysis_message"),
        # toolbar区域  editsql 和 运行
        html.Div(
            [
                fac.AntdButton(
                    # "编辑SQL",
                    id="customAnalysis_editsql",
                    icon=fac.AntdIcon(icon='antd-edit'),
                    type="primary"
                ),
                fac.AntdButton(
                    id="customAnalysis_run",
                    icon=fac.AntdIcon(icon='antd-send'),
                    type="primary"
                ),
                
            ],
            style={
                "display": "flex",
                "justify-content": "flex-start",
                "align-items": "center",
                "gap": 20,
                "padding": "10px",
                "background-color": "#f0f0f0",
                "border-radius": "4px",
                "width": "100%",
                "height": "32px",
            }
        ),
        
        
        
        html.Div(
            [
                html.Div(
                    [
                        fac.AntdSelect(
                            id="customAnalysis_select_wd",
                            allowClear=True,
                            style={
                                "width": "120px",
                            }
                        ),
                        fac.AntdSelect(
                            id="customAnalysis_select_zhb",
                            allowClear=True,
                            style={
                                "width": "120px",
                            }
                        ),
                        fac.AntdButton(
                            "确认",
                            id="customAnalysis_select_btn",
                            type="primary"
                        )
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "flex-start",
                        "align-items": "center",
                        "gap": 20,
                    }
                ),
                html.Div(
                    id="customAnalysis_chart_chart",
                    style={
                        "width": "100%",
                        "height": "300px",
                        "borderRadius": 6,
                        "padding": 8,
                        "margin":"10px 0",
                        "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                        "background": "#ffffff"
                    }
                )
            ],
            id="customAnalysis_chart",
            style={
                "width": "100%",
                "height": "320px",
                "borderRadius": 6,
                "padding": 8,
                "margin":"10px 0",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff"
            }
        ),
        
        # 表格展示
        html.Div(
            [   
                html.H4("表格展示",
                    style={
                        "margin": 8,
                    }
                ),
                fac.AntdTable(
                    id="customAnalysis_table_table",
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
            id="customAnalysis_table",
            style={
                "width": "100%",
                "height": "400px",
                "borderRadius": 6,
                "padding": 8,
                "margin":"10px 0",
                "boxShadow": "0 2px 11px 0 rgba(190, 202, 218, .17)",
                "background": "#ffffff"
            }
        ),
        
        
        # sql 编辑区域
        fac.AntdModal(
            [
                fac.AntdInput(
                    id="customAnalysis_sqlArea",
                    placeholder='SELECT * FROM table; ',
                    mode='text-area',
                    persistence=True,
                    style={
                        "width": '100%',
                        "height": 400,
                    }
                )
            ],
            id='customAnalysis_sqlModal',
            title='sql编辑',
            visible=False,
            renderFooter=True
        )

        
        
        


    ]
)
