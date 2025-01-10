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



def userpathAnalysis_query(userpath_action, user_meet, user_meet_input, datetimerange):
    datetimerange_str = ""
    if datetimerange:
        userpathstarttime, userpathendtime = datetimerange
        datetimerange_str = f"AND (createtime BETWEEN '{userpathstarttime}' AND '{userpathendtime}' )"
    else:
        datetimerange_str = "AND (createtime BETWEEN DATETIME('now', '-30 days') AND DATETIME('now')  )"
        
    # 用户满足条件
    user_meet_str = ""
    if user_meet and user_meet_input:
        with SQLiteClass("./acebergBehavior.db") as cursor:
            user_meet_data = cursor.select_data(
                "realusers",
                "key",
                condition=f"{user_meet} LIKE '%{user_meet_input}%'"
            ) # [{'key': 'user_978f19b4-7267-44bf-b30e-24764eb8dceb'}, ...]
        
        if user_meet_data and len(user_meet_data) < 900:
            user_meet_keys = [f"userKey = '{item['key']}'" for item in user_meet_data]
            user_meet_str = f"AND ({' OR '.join(user_meet_keys)})"
        else:
            user_meet_str = f"AND (1=0)"
    else:
        user_meet_str = ""
    
    
    if userpath_action:
        userpath_action_str = ",\n".join([ f"COUNT(CASE WHEN eventKey = '{item}' THEN 1 END) AS {item}" for item in userpath_action])
        userpath_action_where = " OR ".join([f"eventKey = '{item}'" for item in userpath_action])
        sqlstr = f"""
            SELECT
                {userpath_action_str}
            FROM
                event_to_user
            WHERE
                ({userpath_action_where})
                {datetimerange_str}
                {user_meet_str}
        """
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
            
        return data # [{'app_active': 4, 'app_run': 6}]
    else:
        return []



# 注册userpathAnalysis的回调
def register_callbacks_userpathAnalysis(app):

    # 页面加载 加载options
    @callback(
        Output('userpath-userpath_action', 'options', allow_duplicate=True),
        Output('userpath-user_meet', 'options', allow_duplicate=True),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def userpathAnalysis_page(pathname):
        if pathname == '/userpathAnalysis':
            action_options = event_name_options_query()
            user_meet_options = user_meet_options_query()
            return action_options, user_meet_options
        else:
            return dash.no_update, dash.no_update



    # 重置按钮的回调
    @callback(
        Output('userpath-userpath_action', 'value', allow_duplicate=True),
        Output('userpath-startend', 'value', allow_duplicate=True),
        Output('userpath-user_meet', 'value', allow_duplicate=True),
        Output('userpath-user_meet_input', 'value', allow_duplicate=True),
        Output('userpath-datetimerange', 'value', allow_duplicate=True),
        
        Input('userpathAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def userpathAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None, None,  None
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        

    # 搜索按钮的回调 图表的回调
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userpathAnalysis_chart_sankey'
            ),
            Output('userpathAnalysis_chart_sankey', 'children'),
            Input('userpathAnalysis_chart_sankey', 'data')
    )
    @app.callback(
        Output('userpathAnalysis_chart_sankey', 'data'),
        
        Input('userpathAnalysis-search', 'nClicks'),
        State('userpath-userpath_action', 'value'),
        State('userpath-startend', 'value'),
        State('userpath-user_meet', 'value'),
        State('userpath-user_meet_input', 'value'),
        State('userpath-datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def userpathAnalysis_chart_sankey(nClicks, userpath_action, startend, user_meet, user_meet_input, datetimerange):
        if nClicks and nClicks > 0:
            data = userpathAnalysis_query(userpath_action, user_meet, user_meet_input, datetimerange)
            

            if data and not all(value == 0 for value in data[0].values()):
                nodes = []
                links = []
                
                if startend == 'forstart':
                    nodes = [{"name": "start"}] + [{"name": item} for item in data[0].keys()]
                    # [ {"name": "start"}, {"name": "app_run"}, {"name": "app_active"}]
                    links = [{
                        "source": item["name"],
                        "target": nodes[index + 1]["name"],
                        "value": data[0][nodes[index + 1]["name"]]
                    } if index < len(nodes) - 1 else {} for index, item in enumerate(nodes)]
                    
                else:
                    nodes = [{"name": item} for item in data[0].keys()] + [{"name": "end"}] 
                    # [{"name": "app_run"}, {"name": "app_active"}, {"name": "end"} ]
                    links = [{
                        "source": item["name"],
                        "target": nodes[index+1]["name"],
                        "value": data[0][nodes[index]["name"]]
                    } if index < len(nodes) - 1 else {} for index, item in enumerate(nodes)]
                    
                    
                res = {
                    "nodes": nodes,
                    "links": links
                }
                return res
            else:
                return {}
        else:
            return dash.no_update
        