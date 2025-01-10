import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json
import numpy as np
from datetime import datetime, timedelta



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



def judge_dynamic_query(first_action, earn_action, user_meet, user_meet_input, datetimerange):
        
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
            
    
    earn_action_str = ""
    if earn_action:
        
        earn_action_select = ",\n".join([f"COUNT(CASE WHEN earn_action_eventKey = '{item}' THEN 1 END) as {item}" for item in earn_action])
        
        earn_action_conditions = " OR ".join([f"eventKey = '{action.strip()}'" for action in earn_action])
        earn_action_str = f"""
            WHERE
                {earn_action_conditions}
                {user_meet_str}
                AND (createtime BETWEEN '{datetimerange[0]}' AND '{datetimerange[1]}')
        """if datetimerange else f"""
            WHERE
                {earn_action_conditions}
                {user_meet_str}
            """
        
    
    if first_action and earn_action:
        if datetimerange:
            starttime, endtime = datetimerange
            ltvsql = f"""
                SELECT
                    tempdatetable.date as date,
                    COUNT(first_action_table.first_action_eventKey) as {first_action},
                    {earn_action_select}
                FROM
                    (
                        WITH RECURSIVE date_range(date) AS (
                        SELECT date(strftime('%Y-%m-%d', '{starttime}'), '-6 days')
                        UNION ALL
                        SELECT date(date, '+1 day')
                        FROM date_range
                        WHERE date > date(strftime('%Y-%m-%d', '{starttime}'), '-7 days') AND date < date(strftime('%Y-%m-%d', '{endtime}'), '+7 days')
                    )
                    SELECT * FROM date_range
                    ) as tempdatetable
                LEFT JOIN
                    (
                    SELECT
                        strftime('%Y-%m-%d', createtime) as date,
                        eventKey as first_action_eventKey
                    FROM
                        event_to_user
                    WHERE
                        eventKey = '{first_action}'
                        {user_meet_str}
                        AND (createtime BETWEEN '{starttime}' AND '{endtime}')
                    ) as first_action_table
                ON tempdatetable.date = first_action_table.date
                LEFT JOIN
                (
                SELECT
                    strftime('%Y-%m-%d', createtime) as date,
                    eventKey as earn_action_eventKey
                FROM
                    event_to_user
                {earn_action_str}
                ) as earn_action_table
                ON tempdatetable.date = earn_action_table.date
                GROUP BY tempdatetable.date
            """
            
        else:
            ltvsql = f"""
                SELECT
                    tempdatetable.date as date,
                    COUNT(first_action_table.first_action_eventKey) as {first_action},
                    {earn_action_select}
                FROM
                    (
                        WITH RECURSIVE date_range(date) AS (
                        SELECT date('now', '-6 days')
                        UNION ALL
                        SELECT date(date, '+1 day')
                        FROM date_range
                        WHERE date > date('now', '-7 days') AND date < date('now', '+7 days')
                    )
                    SELECT * FROM date_range
                    ) as tempdatetable
                LEFT JOIN
                    (
                    SELECT
                        strftime('%Y-%m-%d', createtime) as date,
                        eventKey as first_action_eventKey
                    FROM
                        event_to_user
                    WHERE
                        eventKey = '{first_action}'
                        {user_meet_str}
                    ) as first_action_table
                ON tempdatetable.date = first_action_table.date
                LEFT JOIN
                (
                SELECT
                    strftime('%Y-%m-%d', createtime) as date,
                    eventKey as earn_action_eventKey
                FROM
                    event_to_user
                {earn_action_str}
                ) as earn_action_table
                ON tempdatetable.date = earn_action_table.date
                GROUP BY tempdatetable.date
            """
        
            
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                ltvsql
            )
        
        
        rawcolumn = ["date", first_action] + [f"{action}_LTV{i}" for action in earn_action for i in range(1, 8)]
        column = [
        {
            'title': item.split('_LTV')[0],
            'dataIndex': item,
            'group': [item.split('_')[-1]]
        }
        if "_LTV" in item else
        {
            'title': item,
            'dataIndex': item
        }
        for item in rawcolumn]
        
        datares = [
                    {
                        "date": item["date"],
                        f"{first_action}": item[f"{first_action}"],
                        **{f"{jtem}_LTV{i}": sum(xtem.get(f"{jtem}", 0) for xtem in data if jtem in list(xtem.keys())[2:] and xtem["date"]>=item["date"] and xtem["date"] < (datetime.strptime(item["date"], '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')) for jtem in earn_action for i in range(1, 8)}
                    }
                    if item[f"{first_action}"]
                    else {
                       "date": item["date"],
                       f"{first_action}": 0,
                       **{f"{jtem}_LTV{i}": 0 for jtem in earn_action for i in range(1, 8)}
                    } 
                   for item in data]

                
        return column, datares

    else:
        return [], []

# 搜索后的查询方法
def LTVAnalysis_query(first_action, earn_action, user_meet, user_meet_input, datetimerange):
    res = judge_dynamic_query(first_action, earn_action, user_meet, user_meet_input, datetimerange)

    return res





# 注册LTVAnalysis的回调
def register_callbacks_LTVAnalysis(app):

    # 页面加载 加载options
    @callback(
        Output('ltv-first_action', 'options', allow_duplicate=True),
        Output('ltv-earn_action', 'options', allow_duplicate=True),
        Output('ltv-user_meet', 'options', allow_duplicate=True),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def LTVAnalysis_page(pathname):
        if pathname == '/LTVAnalysis':
            options = event_name_options_query()
            user_meet_options = user_meet_options_query()
            return options, options, user_meet_options
        else:
            return dash.no_update, dash.no_update, dash.no_update



    # 搜索按钮的回调
    @callback(
        Output('LTVAnalysis_table_table', 'columns'),
        Output('LTVAnalysis_table_table', 'data'),
        
        Input('LTVAnalysis-search', 'nClicks'),
        State('ltv-first_action', 'value'),
        State('ltv-earn_action', 'value'),
        State('ltv-user_meet', 'value'),
        State('ltv-user_meet_input', 'value'),
        State('ltv-datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def LTVAnalysis_search(nClicks, first_action, earn_action, user_meet, user_meet_input, datetimerange):
        if nClicks and nClicks > 0:
            return LTVAnalysis_query(first_action, earn_action, user_meet, user_meet_input, datetimerange)

        else:
            return dash.no_update, dash.no_update



    # 重置按钮的回调
    @callback(
        Output('ltv-first_action', 'value', allow_duplicate=True),
        Output('ltv-earn_action', 'value', allow_duplicate=True),
        Output('ltv-user_meet', 'value', allow_duplicate=True),
        Output('ltv-user_meet_input', 'value', allow_duplicate=True),
        Output('ltv-datetimerange', 'value', allow_duplicate=True),
        
        Input('LTVAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def LTVAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None, None, None
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        
        
        
        
        
    