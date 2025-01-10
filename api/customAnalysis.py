import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import numpy as np
from datetime import datetime, timedelta



# 自定义分析
def customAnalysis_query(sqlstr):
    try:
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
        )
        return True, data
    
    except Exception as e:
        return False, []


def customAnalysis_chartData(data, wd, zhb):
    # 汇总 y 值
    summary = {}
    
    for item in data:
        x_value = item[wd]
        y_value = item[zhb]
        if x_value in summary:
            summary[x_value] += 1 if y_value else 0
        else:
            summary[x_value] = 1 if y_value else 0

    # 将汇总结果转换为列表
    x = list(summary.keys())
    y = list(summary.values())
    
    res = {
        "x": x,
        "y": y
    }
    
    return res
    
        



# 注册customAnalysis的回调
def register_callbacks_customAnalysis(app):
    
    @app.callback(
        Output('customAnalysis_sqlModal', 'visible'),

        Input('customAnalysis_editsql', 'nClicks'),
        prevent_initial_call=True,
    )
    def customAnalysis_sqlModal(nClicks):
        if nClicks and nClicks > 0:
            return True
        else:
            return False
        
        
    # 点击运行
    @app.callback(
        Output('customAnalysis_message', 'children'),
        Output('customAnalysis_select_wd', 'value'),
        Output('customAnalysis_select_zhb', 'value'),
        Output('customAnalysis_select_wd', 'options'),
        Output('customAnalysis_select_zhb', 'options'),
        Output('customAnalysis_table_table', 'columns'),
        Output('customAnalysis_table_table', 'data'),

        Input('customAnalysis_run', 'nClicks'),
        State('customAnalysis_sqlArea', 'value'),
        prevent_initial_call=True,
    )
    def customAnalysis_run(nClicks, sqlstr):
        if nClicks and nClicks > 0:
            data = customAnalysis_query(sqlstr)
            flag, resdata = data
            
            if flag and resdata:
                # 存储查询结果以供后续使用
                global global_data
                global_data = resdata  # 存储结果
                
                columns = [
                    {
                        "title": item,
                        "dataIndex": item,
                        "renderOptions": {
                            "renderType": "ellipsis",
                        }
                    }
                    for item in resdata[0].keys()]
                options = [
                {
                    'value': item,
                    'label': item,
                }
                    for item in resdata[0]]
                
                
                return None, None, None, options, options, columns, resdata
            
            else:
                return fac.AntdMessage(content='执行错误, 请检查SQL语句', type='error'), None, None, [], [], [], []
        
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
    

    
    # customAnalysis_chart_chart
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_customAnalysis_chart_chart'
            ),
            Output('customAnalysis_chart_chart', 'children'),
            Input('customAnalysis_chart_chart', 'data')
    )
    @app.callback(
        Output('customAnalysis_chart_chart', 'data'),
        Input('customAnalysis_select_btn', 'nClicks'),
        State('customAnalysis_select_wd', 'value'),
        State('customAnalysis_select_zhb', 'value'),
        prevent_initial_call=True,
    )
    def customAnalysis_chart_chart(nClicks, wd, zhb):
        if nClicks and nClicks > 0 and wd and zhb:

            res = customAnalysis_chartData(global_data, wd, zhb)
            return res
        else:
            return dash.no_update



    
