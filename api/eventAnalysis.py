import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import numpy as np



# def eventAnalysis_chart_Tagtable_query(tag_name, datatype, 
#                             createmethod, status ,current,condition="isdel='0'"):
#     with SQLiteClass("./acebergBehavior.db") as cursor:
#         columns = cursor.select_columns(
#             "tagManage",
#             "*"
#         )
#         if columns:
#             res_columns = [
#                 {
#                 "dataIndex": 'key',
#                 "title": 'key',
#                 "renderOptions": {"renderType": "ellipsis"},
#                 }
#             ]
#             for item in columns:
#                 if item !="key":
#                     res_columns.append({
#                         "dataIndex": item,
#                         "title": item,
#                         "renderOptions": {"renderType": "ellipsis"},
#                     })
#         else:
#             res_columns = []
        
#         condition_str = ""
#         if tag_name:
#             condition_str= condition_str + f" and tag_name like '%{tag_name}%'"
#         if datatype:
#             condition_str = condition_str + f" and datatype = '{datatype}'"
#         if createmethod:
#             condition_str = condition_str + f" and createmethod = '{createmethod}'"
#         if status:
#             condition_str = condition_str + f" and status = '{status}'"
        
#         data = cursor.select_data(
#             "tagManage",
#             "*",
#             condition= condition + condition_str 
#         )
        
#         # total = cursor.select_data(
#         #     "tagManage",
#         #     "*",
#         # )
        
            
#         # pagination = {"current":current, "pageSize":10, "total":len(total)}

#     return res_columns, data #, pagination


# 查询事件名称下拉框
def event_name_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "eventManage",
            "eventKey, eventName"
        )
    res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
    return res

def event_summarymethod_func(data, event_name, event_summarymethod):
    if data and event_summarymethod:
        event_name_values = [item[event_name] for item in data]

        calecute = {
            "sum": sum(event_name_values),
            "ave": sum(event_name_values) / len(event_name_values),
            "max": max(event_name_values),
            "min": min(event_name_values),
            "distinct": len(set(event_name_values)),
            "q1": np.percentile(event_name_values, 25),
            "q3": np.percentile(event_name_values, 75),
            "median": np.median(event_name_values),
            "p90": np.percentile(event_name_values, 90),
            "p95": np.percentile(event_name_values, 95),
            "p99": np.percentile(event_name_values, 99)
        }

        # 打印结果
        res = [{
            f"{event_name}": calecute[event_summarymethod]
        }]
        
        return res
    else:
        return data
        



# 搜索去查询数据
def eventAnalysis_clicksearch_query(event_name, event_where, event_summarymethod):
    sqlstr = ''
    event_where_list = ["total_num", "ave_num", "total_num_currentmonth",
                        "total_num_last7", "total_num_last30"]
    if event_name and event_where in event_where_list and not event_summarymethod:

        if event_where == "total_num":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}'
                '''
                
        elif event_where == "ave_num":
            sqlstr = f'''
                SELECT ROUND(COUNT(eventKey) * 1.0 / count(DISTINCT(userKey)), 2) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}'
                '''
            
        elif event_where == "total_num_currentmonth":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and strftime('%Y-%m', createtime) = strftime('%Y-%m', 'now')
                '''
            
        elif event_where == "total_num_last7":
            
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-7 days', 'localtime')
            '''
            
        elif event_where == "total_num_last30":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-30 days', 'localtime')
            '''
        with SQLiteClass("./acebergBehavior.db") as cursor:
            res = cursor.custom_sql(sqlstr)

        result = {
            "x": list(res[0].keys()) if res else [],  
            "y": [list(i.values())[0] for i in res] 
        }
        return result
            
            
    elif event_name and event_where not in event_where_list and event_summarymethod:

        if event_where == "user_num":
            sqlstr = f'''
                SELECT userKey, userAccount, count(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}'
                '''
        elif event_where == "user_num_currentmonth":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and strftime('%Y-%m', createtime) = strftime('%Y-%m', 'now')
            '''
        elif event_where == "user_num_last7":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-7 days', 'localtime')
            '''
        elif event_where == "user_num_last30":
            sqlstr = f'''
                SELECT COUNT(eventKey) AS {event_name}
                FROM event_to_user
                WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-30 days', 'localtime')
            '''
        

        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(sqlstr)
        
        res = event_summarymethod_func(data, event_name, event_summarymethod)
        
        result = {
            "x": list(res[0].keys()) if res else [],  
            "y": [list(i.values())[0] for i in res] 
        }
        return result




# 注册eventAnalysis的回调
def register_callbacks_eventAnalysis(app):
    # eventname 的options
    @app.callback(
        Output('event_name', 'options'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_event_name_options(pathname):
        res = event_name_options_query()
        return res

    # event_where 的options
    @app.callback(
        Output('event_where', 'options'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_event_where_options(pathname):
        res = [
            {"label": "总次数", "value": "total_num"},
            {"label": "人均次数", "value": "ave_num"},
            {"label": "当月总次数", "value": "total_num_currentmonth"},
            {"label": "过去7天总次数", "value": "total_num_last7"},
            {"label": "过去30天总次数", "value": "total_num_last30"},
            
            
            {"label": "用户数", "value": "user_num"},
            {"label": "当月用户数", "value": "user_num_currentmonth"},
            {"label": "过去7天用户数", "value": "user_num_last7"},
            {"label": "过去30天用户数", "value": "user_num_last30"},
        ]
        return res


    # event_summarymethod 的options
    @app.callback(
        Output('event_summarymethod', 'options'),
        Input('event_where', 'value'),
        prevent_initial_call=True,
    )
    def eventAnalysis_event_summarymethod_options(value):
        if value == "user_num" or value == "user_num_currentmonth" or value == "user_num_last7" or value == "user_num_last30":
            options = [
                            {"label": "总和", "value": "sum"},
                            {"label": "均值", "value": "ave"},
                            {"label": "最大值", "value": "max"},
                            {"label": "最小值", "value": "min"},
                            {"label": "去重数", "value": "distinct"},
                            {"label": "下四分位数", "value": "q1"},
                            {"label": "中位数", "value": "median"},
                            {"label": "上四分位数", "value": "q3"},
                            {"label": "P90", "value": "p90"},
                            {"label": "P95", "value": "p95"},
                            {"label": "P99", "value": "p99"},
            ]
            return options
        else:
            return []
        
    # 切换时清空已有value
    @app.callback(
        Output('event_summarymethod', 'value', allow_duplicate=True),
        Input('event_where', 'value'),
        prevent_initial_call=True,
    )
    def eventAnalysis_event_summarymethod_options(value):
        return ''
        
        
    # 重置按钮的回调
    @app.callback(
        Output('event_name', 'value'),
        Output('event_where', 'value'),
        Output('event_summarymethod', 'value'),
        Input('eventAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def eventAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return '', '', ''
        
        
        

    # eventAnalysis_chart_eventbarline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_eventbarline'
            ),
            Output('eventAnalysis_chart_eventbarline', 'children'),
            Input('eventAnalysis_chart_eventbarline', 'data')
    )
    @app.callback(
        Output('eventAnalysis_chart_eventbarline', 'data'),
        Input('eventAnalysis-search', 'nClicks'),
        State('event_name', 'value'),
        State('event_where', 'value'),
        State('event_summarymethod', 'value'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_eventbarline(nClicks, event_name, event_where, event_summarymethod):
        if nClicks and nClicks > 0:
            res = eventAnalysis_clicksearch_query(event_name, event_where, event_summarymethod)
            return res
        else:
            return dash.no_update
    
    

    # eventAnalysis_chart_Tagtable
    @app.callback(
        Output('eventAnalysis_chart_eventTable_table', 'columns'),
        Output('eventAnalysis_chart_eventTable_table', 'data'),
        Input('eventAnalysis-search', 'nClicks'),
        State('event_name', 'value'),
        State('event_where', 'value'),
        State('event_summarymethod', 'value'),
        
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Tagtable(nClicks, event_name, event_where, event_summarymethod):
        if nClicks and nClicks > 0:
            res = eventAnalysis_clicksearch_query(event_name, event_where, event_summarymethod)

            column = [{
                "dataIndex": res['x'][0] if res else 'unknown',
                "title": res['x'][0] if res else 'unknown',
                "renderOptions": {"renderType": "ellipsis"},
            }]
            data = [{
                res['x'][0] if res else 'unknown': res['y'][0] if res else 'unknown'
            }]
            return column, data
        else:
            return dash.no_update, dash.no_update
        
        


    # eventAnalysis_chart_eventGrouppie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_eventGrouppie'
            ),
            Output('eventAnalysis_chart_eventGrouppie', 'children'),
            Input('eventAnalysis_chart_eventGrouppie', 'data')
    )
    @app.callback(
        Output('eventAnalysis_chart_eventGrouppie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_eventGrouppie(pathname):
        res = [
            { 'value': 1048, 'name': 'APP启动' },
            { 'value': 550, 'name': 'APP退出' },
            { 'value': 475, 'name': 'APP浏览页面' },
            { 'value': 300, 'name': 'APP元素点击' },
            { 'value': 238, 'name': '其他' },
        ]
        return res
    
    
    
    # eventAnalysis_chart_Importanteventcoverbar
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Importanteventcoverbar'
            ),
            Output('eventAnalysis_chart_Importanteventcoverbar', 'children'),
            Input('eventAnalysis_chart_Importanteventcoverbar', 'data'),
            Input('eventAnalysis_chart_Importanteventcoverbar', 'years'),
            Input('eventAnalysis_chart_Importanteventcoverbar', 'datatypenum'),
    )
    @callback(
        Output('eventAnalysis_chart_Importanteventcoverbar', 'data'),
        Output('eventAnalysis_chart_Importanteventcoverbar', 'years'),
        Output('eventAnalysis_chart_Importanteventcoverbar', 'datatypenum'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Importanteventcoverbar(pathname):
        data = [
            [
                "coverusercount",
                "Tag",
                "datetime"
            ],
            [815,"app_run",20241101],[1314, "login",20241101],
            [314, "app_overviewpage",20241101],[2314, "app_eleclick",20241101],
            [1814, "app_exit",20241101],
            
            [765,"app_run",20241102],[1214, "login",20241102],
            [214, "app_overviewpage",20241102],[2014, "app_eleclick",20241102],
            [2114, "app_exit",20241102],
            
            [705,"app_run",20241103],[1100, "login",20241103],
            [174, "app_overviewpage",20241103],[1614, "app_eleclick",20241103],
            [514, "app_exit",20241103],
            
            [645,"app_run",20241104],[914, "login",20241104],
            [123, "app_overviewpage",20241104],[614, "app_eleclick",20241104],
            [2333, "app_exit",20241104],
        ]
        years = ["datetime", 20241101, 20241102, 20241103, 20241104]
        datatypenum = 4
        return data, years, datatypenum








    # eventAnalysis_chart_Agecutline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Agecutline'
            ),
            Output('eventAnalysis_chart_Agecutline', 'children'),
            Input('eventAnalysis_chart_Agecutline', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Agecutline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Agecutline(pathname):
        res = {
            'x': ['0-18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    

    # eventAnalysis_chart_Vipline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Vipline'
            ),
            Output('eventAnalysis_chart_Vipline', 'children'),
            Input('eventAnalysis_chart_Vipline', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Vipline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Vipline(pathname):
        res = {
            'x': ['vip0', 'vip1', 'vip2', 'vip3', 'vip4', 'vip5', 'vip6'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    
      
    # eventAnalysis_chart_Genderpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Genderpie'
            ),
            Output('eventAnalysis_chart_Genderpie', 'children'),
            Input('eventAnalysis_chart_Genderpie', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Genderpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Genderpie(pathname):
        res = [
            { 'value': 1048, 'name': '男(Male)' },
            { 'value': 735, 'name': '女(Female)' },
        ]
        return res
    
    # eventAnalysis_chart_Sourcepie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Sourcepie'
            ),
            Output('eventAnalysis_chart_Sourcepie', 'children'),
            Input('eventAnalysis_chart_Sourcepie', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Sourcepie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Sourcepie(pathname):
        
        res = [
            { 'value': 1048, 'name': 'Google Ads' },
            { 'value': 735, 'name': '官网' },
            { 'value': 580, 'name': '抖音' },
            { 'value': 484, 'name': '百度' },
            { 'value': 300, 'name': '腾讯新闻' },
            { 'value': 200, 'name': 'Video Ads' },
            { 'value': 180, 'name': '朋友推荐' },
            { 'value': 120, 'name': 'Others' }
        ]
        return res
    
    
    # eventAnalysis_chart_Careerpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Careerpie'
            ),
            Output('eventAnalysis_chart_Careerpie', 'children'),
            Input('eventAnalysis_chart_Careerpie', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Careerpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Careerpie(pathname):
        res = [
            { 'value': 1048, 'name': '工程师' },
            { 'value': 735, 'name': '医生' },
            { 'value': 580, 'name': '教师' },
            { 'value': 484, 'name': '公务员' },
            { 'value': 300, 'name': '自由职业' },
            { 'value': 200, 'name': '个体户' },
            { 'value': 180, 'name': '民企职员' },
            { 'value': 120, 'name': '国企职员' },
            { 'value': 120, 'name': '会计' },
            { 'value': 120, 'name': '其他' }
        ]
        return res
    
    
    # eventAnalysis_chart_OSpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_OSpie'
            ),
            Output('eventAnalysis_chart_OSpie', 'children'),
            Input('eventAnalysis_chart_OSpie', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_OSpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_OSpie(pathname):
        
        res = [
            { 'value': 9048, 'name': 'Windows' },
            { 'value': 2735, 'name': 'IOS' },
            { 'value': 3580, 'name': 'MacOS' },
            { 'value': 2484, 'name': 'Android' },
            { 'value': 6300, 'name': 'Linux' }
        ]
        return res
    


    # eventAnalysis_chart_Activityline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_eventAnalysis_chart_Activityline'
            ),
            Output('eventAnalysis_chart_Activityline', 'children'),
            Input('eventAnalysis_chart_Activityline', 'data'),
    )
    @app.callback(
        Output('eventAnalysis_chart_Activityline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventAnalysis_chart_Activityline(pathname):
        res = {
            'x': ['202312', '202401', '202402', '202403', '202404', '202405', '202406', '202407',
            '202408', '202409', '202410', '202411'],
            'y': [ int(random.random()*200)+6 for i in range(12)]
        }
        return res
    
    
    