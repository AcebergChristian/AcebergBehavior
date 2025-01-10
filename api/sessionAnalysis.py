import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import numpy as np
from datetime import datetime, timedelta



# session 名称下拉框
def session_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "session_to_user",
            "sessionKey, sessionName"
        )
    res = [{"label": item["sessionName"], "value": item["sessionKey"]} for item in data]
    return res


# 查询事件名称下拉框
def event_name_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "eventManage",
            "eventKey, eventName"
        )
    res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
    return res


# 用户筛选 options 查询
def user_meet_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        columns = cursor.select_columns(
            "realusers"
        )
    columns_filter = [{"label": item, "value": item} for item in columns if item not in ['key', 'account', 'password', 'role', 'isdel', 'creator', 'createtime']]
    return columns_filter



def sessionAnalysis_query(session_action, indi_action, user_meet, user_meet_input, datetimerange):
    datetimerange_str = ""
    if datetimerange:
        sessionstarttime, sessionendtime = datetimerange
        datetimerange_str = f"createtime BETWEEN '{sessionstarttime}' AND '{sessionendtime}'"
    else:
        datetimerange_str = "(1=1)"
        
    # 用户满足条件
    user_meet_str = ""
    if user_meet and user_meet_input:
        with SQLiteClass("./acebergBehavior.db") as cursor:
            user_meet_data = cursor.select_data(
                "realusers",
                "key",
                condition=f"{user_meet} LIKE '%{user_meet_input}%'"
            ) # [{'key': 'user_978f19b4-7267-44bf-b30e-24764eb8dceb'}, ...]
        if user_meet_data:
            user_meet_str_in = ""
            for index, item in enumerate(user_meet_data):
                if index == len(user_meet_data) - 1:
                    user_meet_str_in += f"userKey = '{item['key']}'"
                else:
                    user_meet_str_in += f"userKey = '{item['key']}' OR "
                    
            user_meet_str = f"AND ({user_meet_str_in})"
        else:
            user_meet_str = f"AND (1=0)"
    else:
        user_meet_str = ""
    
    
    # 拼接 indi_action_str
    indi_action_str = ",\n".join([ f"SUM(CASE WHEN event_table.eventKey='{item}' THEN 1 ELSE 0 END) as {item}" for item in indi_action]) if indi_action else ""

    if session_action and indi_action:
        sqlstr = f"""
            SELECT 
                STRFTIME('%Y-%m-%d', event_table.createtime) as date,
                {indi_action_str}
            FROM
                (
                    SELECT
                        eventKey,
                        userKey,
                        userAccount,
                        createtime
                    FROM
                        event_to_user
                    WHERE
                        {datetimerange_str}
                        {user_meet_str}
                ) as event_table
            LEFT JOIN
                (
                    SELECT
                        sessionKey,
                        sessionName,
                        userKey,
                        userAccount,
                        starttime,
                        endtime
                    FROM 
                        session_to_user
                ) as session_table
            ON event_table.userAccount = session_table.userAccount AND
                event_table.createtime >= session_table.starttime AND
                event_table.createtime <= session_table.endtime
            WHERE session_table.starttime is NOT NULL
            GROUP BY STRFTIME('%Y-%m-%d', event_table.createtime)
        """
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
            
    else:
        data = []

    return data



# 注册sessionAnalysis的回调
def register_callbacks_sessionAnalysis(app):

    # 页面加载 加载options
    @callback(
        Output('session-session_action', 'options', allow_duplicate=True),
        Output('session-indi_action', 'options', allow_duplicate=True),
        Output('session-user_meet', 'options', allow_duplicate=True),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def sessionAnalysis_page(pathname):
        if pathname == '/sessionAnalysis':
            session_options = session_options_query()
            action_options = event_name_options_query()
            user_meet_options = user_meet_options_query()
            return session_options, action_options, user_meet_options
        else:
            return dash.no_update, dash.no_update, dash.no_update



    # 搜索按钮的回调
    @callback(
        Output('sessionAnalysis_table_table', 'columns'),
        Output('sessionAnalysis_table_table', 'data'),
        
        Input('sessionAnalysis-search', 'nClicks'),
        State('session-session_action', 'value'),
        State('session-indi_action', 'value'),
        State('session-user_meet', 'value'),
        State('session-user_meet_input', 'value'),
        State('session-datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def sessionAnalysis_search(nClicks, session_action, indi_action, user_meet, user_meet_input, datetimerange):
        if nClicks and nClicks > 0:
            data = sessionAnalysis_query(session_action, indi_action, user_meet, user_meet_input, datetimerange)
            column = [
            {
                'title': item,
                'dataIndex': item
            } for item in data[0].keys() ] if data else []
            return column, data
        
        else:
            return dash.no_update, dash.no_update



    # 重置按钮的回调
    @callback(
        Output('session-session_action', 'value', allow_duplicate=True),
        Output('session-indi_action', 'value', allow_duplicate=True),
        Output('session-user_meet', 'value', allow_duplicate=True),
        Output('session-user_meet_input', 'value', allow_duplicate=True),
        Output('session-datetimerange', 'value', allow_duplicate=True),
        
        Input('sessionAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def sessionAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None, None, None
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        

    # 图表的回调
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_sessionAnalysis_chart_barline'
            ),
            Output('sessionAnalysis_chart_barline', 'children'),
            Input('sessionAnalysis_chart_barline', 'res')
    )
    @app.callback(
        Output('sessionAnalysis_chart_barline', 'res'),
        Input('sessionAnalysis-search', 'nClicks'),
        State('session-session_action', 'value'),
        State('session-indi_action', 'value'),
        State('session-user_meet', 'value'),
        State('session-user_meet_input', 'value'),
        State('session-datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def sessionAnalysis_chart_eventbarline(nClicks, session_action, indi_action, user_meet, user_meet_input, datetimerange):
        if nClicks and nClicks > 0:
            data = sessionAnalysis_query(session_action, indi_action, user_meet, user_meet_input, datetimerange)
            
            if not data:
                return {"xData":[], "seriesData":[] }
            
            xData = [item["date"] for item in data]
            seriesData = []
            for item in data[0].keys():
                if item == "date":
                    continue
                seriesData.append({
                    "name": item,
                    "data": [d[item] for d in data],
                    "type": "line",
                    "smooth": True
                })
            
            res = {
                "xData":xData,
                "seriesData":seriesData
            }
            
            print(res)
            return res
        else:
            return dash.no_update, dash.no_update
        