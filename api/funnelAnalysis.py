import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import numpy as np



# 查询事件名称下拉框
def event_name_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "eventManage",
            "eventKey, eventName"
        )
    res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
    return res



def funnelAnalysis_query(eventnamelist, datarange):
    wherestr = f"""(
    {' or '.join([f"eventKey='{item}'" for item in eventnamelist])}
    )
    """
    
    if datarange:
        wherestr += f" AND createtime BETWEEN '{datarange[0]}' AND '{datarange[1]}'"
    
    sqlstr = f"""
        SELECT json_group_array(json_object('name', eventKey, 'value', count)) AS res
        FROM (
            SELECT eventKey, COUNT(*) AS count
            FROM event_to_user
            where {wherestr}
            GROUP BY eventKey
        ) AS subquery;
    """
    
    
    with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
    res = json.loads(data[0]['res'])
    
    sorted_res = [next(
        (item for item in res if item['name'] == name)
        ,
        {'name': name, 'value': 0}) for name in eventnamelist
    ]
    
    return sorted_res


# 注册funnelAnalysis的回调
def register_callbacks_funnelAnalysis(app):
    # eventname 的options
    @app.callback(
        Output('event_name_list', 'options'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def funnelAnalysis_event_name_options(pathname):
        res = event_name_options_query()
        
        return res



    # 重置按钮的回调
    @app.callback(
        Output('event_name_list', 'value'),
        Output('event_datetime', 'value'),
        Input('funnelAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def funnelAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None
        else:
            return dash.no_update, dash.no_update
        
    
    
    
    # 搜索按钮的回调
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_funnelAnalysis_chart_funnel'
            ),
            Output('funnelAnalysis_chart_funnel', 'children'),
        Input('funnelAnalysis_chart_funnel', 'columns'),
        Input('funnelAnalysis_chart_funnel', 'data'),
    )
    @callback(
        Output('funnelAnalysis_chart_funnel', 'columns'),
        Output('funnelAnalysis_chart_funnel', 'data'),
        Output('funnelAnalysis_chart_funnelTable_table', 'columns'),
        Output('funnelAnalysis_chart_funnelTable_table', 'data'),
        Input('funnelAnalysis-search', 'nClicks'),
        State('event_name_list', 'value'),
        State('event_datetime', 'value'),
        prevent_initial_call=True,
    )
    def funnelAnalysis_reset(nClicks, eventnamelist, datarange):
        if nClicks and nClicks > 0 and eventnamelist:
            res = funnelAnalysis_query(eventnamelist, datarange)
            tablecolumns = []
            tabledataitem = {}
            
            for index, item in enumerate(res):
                
                tablecolumns.append(
                    {
                        "dataIndex": item['name'],
                        "title": item['name'],
                        "renderOptions": {"renderType": "ellipsis"},
                    }
                )
                if index != len(eventnamelist) -1:
                    tablecolumns.append(
                        {
                            "dataIndex": f'transformrate_{index}',
                            "title": 'transformrate',
                            "renderOptions": {"renderType": "ellipsis"}
                        }
                    )
                    
                tabledataitem[item['name']] = item['value']
                if index > 0:
                    tabledataitem[f'transformrate_{index-1}'] = f"{item['value']*100 / res[index - 1]['value']:.4f}%"  if res[index - 1]['value']!=0 else 'None'
            
            
            return eventnamelist, res, tablecolumns, [tabledataitem]
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update























# def funnelAnalysis_chart_Tagtable_query(tag_name, datatype, 
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
# def event_name_options_query():
#     with SQLiteClass("./acebergBehavior.db") as cursor:
#         data = cursor.select_data(
#             "eventManage",
#             "eventKey, eventName"
#         )
#     res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
#     return res

# def event_summarymethod_func(data, event_name, event_summarymethod):
#     if data and event_summarymethod:
#         event_name_values = [item[event_name] for item in data]

#         calecute = {
#             "sum": sum(event_name_values),
#             "ave": sum(event_name_values) / len(event_name_values),
#             "max": max(event_name_values),
#             "min": min(event_name_values),
#             "distinct": len(set(event_name_values)),
#             "q1": np.percentile(event_name_values, 25),
#             "q3": np.percentile(event_name_values, 75),
#             "median": np.median(event_name_values),
#             "p90": np.percentile(event_name_values, 90),
#             "p95": np.percentile(event_name_values, 95),
#             "p99": np.percentile(event_name_values, 99)
#         }

#         # 打印结果
#         res = [{
#             f"{event_name}": calecute[event_summarymethod]
#         }]
        
#         return res
#     else:
#         return data
        



# # 搜索去查询数据
# def funnelAnalysis_clicksearch_query(event_name, event_where, event_summarymethod):
#     sqlstr = ''
#     event_where_list = ["total_num", "ave_num", "total_num_currentmonth",
#                         "total_num_last7", "total_num_last30"]
#     if event_name and event_where in event_where_list and not event_summarymethod:

#         if event_where == "total_num":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}'
#                 '''
                
#         elif event_where == "ave_num":
#             sqlstr = f'''
#                 SELECT ROUND(COUNT(eventKey) * 1.0 / count(DISTINCT(userKey)), 2) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}'
#                 '''
            
#         elif event_where == "total_num_currentmonth":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and strftime('%Y-%m', createtime) = strftime('%Y-%m', 'now')
#                 '''
            
#         elif event_where == "total_num_last7":
            
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-7 days', 'localtime')
#             '''
            
#         elif event_where == "total_num_last30":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-30 days', 'localtime')
#             '''
#         with SQLiteClass("./acebergBehavior.db") as cursor:
#             res = cursor.custom_sql(sqlstr)

#         result = {
#             "x": list(res[0].keys()) if res else [],  
#             "y": [list(i.values())[0] for i in res] 
#         }
#         return result
            
            
#     elif event_name and event_where not in event_where_list and event_summarymethod:

#         if event_where == "user_num":
#             sqlstr = f'''
#                 SELECT userKey, userAccount, count(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}'
#                 '''
#         elif event_where == "user_num_currentmonth":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and strftime('%Y-%m', createtime) = strftime('%Y-%m', 'now')
#             '''
#         elif event_where == "user_num_last7":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-7 days', 'localtime')
#             '''
#         elif event_where == "user_num_last30":
#             sqlstr = f'''
#                 SELECT COUNT(eventKey) AS {event_name}
#                 FROM event_to_user
#                 WHERE eventKey = '{event_name}' and createtime >= datetime('now', '-30 days', 'localtime')
#             '''
        

#         with SQLiteClass("./acebergBehavior.db") as cursor:
#             data = cursor.custom_sql(sqlstr)
        
#         res = event_summarymethod_func(data, event_name, event_summarymethod)
        
#         result = {
#             "x": list(res[0].keys()) if res else [],  
#             "y": [list(i.values())[0] for i in res] 
#         }
#         return result




# # 注册funnelAnalysis的回调
# def register_callbacks_funnelAnalysis(app):
#     # eventname 的options
#     @app.callback(
#         Output('event_name', 'options'),
#         Input('url', 'pathname'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_event_name_options(pathname):
#         res = event_name_options_query()
#         return res

#     # event_where 的options
#     @app.callback(
#         Output('event_where', 'options'),
#         Input('url', 'pathname'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_event_where_options(pathname):
#         res = [
#             {"label": "总次数", "value": "total_num"},
#             {"label": "人均次数", "value": "ave_num"},
#             {"label": "当月总次数", "value": "total_num_currentmonth"},
#             {"label": "过去7天总次数", "value": "total_num_last7"},
#             {"label": "过去30天总次数", "value": "total_num_last30"},
            
            
#             {"label": "用户数", "value": "user_num"},
#             {"label": "当月用户数", "value": "user_num_currentmonth"},
#             {"label": "过去7天用户数", "value": "user_num_last7"},
#             {"label": "过去30天用户数", "value": "user_num_last30"},
#         ]
#         return res


#     # event_summarymethod 的options
#     @app.callback(
#         Output('event_summarymethod', 'options'),
#         Input('event_where', 'value'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_event_summarymethod_options(value):
#         if value == "user_num" or value == "user_num_currentmonth" or value == "user_num_last7" or value == "user_num_last30":
#             options = [
#                             {"label": "总和", "value": "sum"},
#                             {"label": "均值", "value": "ave"},
#                             {"label": "最大值", "value": "max"},
#                             {"label": "最小值", "value": "min"},
#                             {"label": "去重数", "value": "distinct"},
#                             {"label": "下四分位数", "value": "q1"},
#                             {"label": "中位数", "value": "median"},
#                             {"label": "上四分位数", "value": "q3"},
#                             {"label": "P90", "value": "p90"},
#                             {"label": "P95", "value": "p95"},
#                             {"label": "P99", "value": "p99"},
#             ]
#             return options
#         else:
#             return []
        
#     # 切换时清空已有value
#     @app.callback(
#         Output('event_summarymethod', 'value', allow_duplicate=True),
#         Input('event_where', 'value'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_event_summarymethod_options(value):
#         return ''
        
        
#     # 重置按钮的回调
#     @app.callback(
#         Output('event_name', 'value'),
#         Output('event_where', 'value'),
#         Output('event_summarymethod', 'value'),
#         Input('funnelAnalysis-reset', 'nClicks'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_reset(nClicks):
#         if nClicks and nClicks > 0:
#             return '', '', ''
        
        
        

#     # funnelAnalysis_chart_eventbarline
#     app.clientside_callback(
#             ClientsideFunction(
#                 namespace='clientside',
#                 function_name='func_funnelAnalysis_chart_eventbarline'
#             ),
#             Output('funnelAnalysis_chart_eventbarline', 'children'),
#             Input('funnelAnalysis_chart_eventbarline', 'data')
#     )
#     @app.callback(
#         Output('funnelAnalysis_chart_eventbarline', 'data'),
#         Input('funnelAnalysis-search', 'nClicks'),
#         State('event_name', 'value'),
#         State('event_where', 'value'),
#         State('event_summarymethod', 'value'),
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_chart_eventbarline(nClicks, event_name, event_where, event_summarymethod):
#         if nClicks and nClicks > 0:
#             res = funnelAnalysis_clicksearch_query(event_name, event_where, event_summarymethod)
#             return res
#         else:
#             return dash.no_update
    
    

#     # funnelAnalysis_chart_Tagtable
#     @app.callback(
#         Output('funnelAnalysis_chart_eventTable_table', 'columns'),
#         Output('funnelAnalysis_chart_eventTable_table', 'data'),
#         Input('funnelAnalysis-search', 'nClicks'),
#         State('event_name', 'value'),
#         State('event_where', 'value'),
#         State('event_summarymethod', 'value'),
        
#         prevent_initial_call=True,
#     )
#     def funnelAnalysis_chart_Tagtable(nClicks, event_name, event_where, event_summarymethod):
#         if nClicks and nClicks > 0:
#             res = funnelAnalysis_clicksearch_query(event_name, event_where, event_summarymethod)

#             column = [{
#                 "dataIndex": res['x'][0] if res else 'unknown',
#                 "title": res['x'][0] if res else 'unknown',
#                 "renderOptions": {"renderType": "ellipsis"},
#             }]
#             data = [{
#                 res['x'][0] if res else 'unknown': res['y'][0] if res else 'unknown'
#             }]
#             return column, data
#         else:
#             return dash.no_update, dash.no_update
        
        





    