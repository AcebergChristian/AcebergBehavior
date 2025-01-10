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


# 用户筛选 options 查询
def user_filter_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        columns = cursor.select_columns(
            "realusers"
        )
    columns_filter = [{"label": item, "value": item} for item in columns if item not in ['key', 'account', 'password', 'role', 'isdel', 'creator', 'createtime']]
    return columns_filter




# 搜索后的查询方法
def retentionAnalysis_query(first_event, second_event, other_event, user_filter, user_filter_input, datetimerange):
    user_filter_str = ""
    if user_filter and user_filter_input:
        with SQLiteClass("./acebergBehavior.db") as cursor:
            user_filter_data = cursor.select_data(
                "realusers",
                "key",
                condition=f"{user_filter} LIKE '%{user_filter_input}%'"
            ) # [{'key': 'user_978f19b4-7267-44bf-b30e-24764eb8dceb'}, ...]
        user_filter_str_in = ""
        for index, item in enumerate(user_filter_data):
            if index == len(user_filter_data) - 1:
                user_filter_str_in += f"userKey = '{item['key']}'"
            else:
                user_filter_str_in += f"userKey = '{item['key']}' OR "
                
        user_filter_str = f"AND ({user_filter_str_in})"
    
    
    
    other_event_select_str = "" # select 的动态
    other_event_str = "" # 左链接的字符串
    
    if not datetimerange:
        datetimerange_str = "AND createtime >= date('now', '-6 days')"
    else:
        start_date, end_date = datetimerange
        datetimerange_str = f"AND createtime BETWEEN '{start_date}' AND '{end_date}'"
    if other_event:
        for item in other_event:
            other_event_select_str += f"""
            ,
                CASE
                    WHEN {item}table.count THEN {item}table.count
                    ELSE 0
                END as {item}
            """
    
    
            other_event_str += f"""
                LEFT JOIN  
                (
                    SELECT 
                        strftime('%Y-%m-%d', createtime) as date, 
                        eventKey, 
                        count(eventKey) as count
                    FROM
                        event_to_user
                    WHERE
                        eventKey = '{item}'
                        {datetimerange_str}
                        {user_filter_str}
                    GROUP BY
                        strftime('%Y-%m-%d', createtime)
                ) as {item}table
                ON tempdatetable.date = {item}table.date
            """
    
    
    
            
    
    # first_event, second_event 必选
    if first_event and second_event:
        # 如果没有提供日期范围，默认查询近7天
        if not datetimerange:
            sqlstr = f"""
                SELECT 
                    tempdatetable.date as date,
                    CASE
                        WHEN datatable1.count THEN datatable1.count
                        ELSE 0
                    END as {first_event},
                    CASE
                        WHEN datatable2.count THEN datatable2.count
                        ELSE 0
                    END as {second_event},
                    CASE 
                        WHEN datatable1.count
                        THEN CAST(ROUND((COALESCE(datatable2.count, 0) / CAST(datatable1.count AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as retention_rate
                    {other_event_select_str}
                    
                FROM
                    (
                        WITH RECURSIVE date_range(date) AS (
                            SELECT date('now', '-6 days')
                            UNION ALL
                            SELECT date(date, '+1 day')
                            FROM date_range
                            WHERE date < date('now')
                        )
                        SELECT * FROM date_range
                    ) as tempdatetable
                    LEFT JOIN  
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date, 
                            eventKey, 
                            count(eventKey) as count
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{first_event}'
                            AND createtime >= date('now', '-6 days')
                            {user_filter_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as datatable1
                    ON tempdatetable.date = datatable1.date
                    LEFT JOIN  
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date, 
                            eventKey, 
                            count(eventKey) as count
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{second_event}'
                            AND createtime >= date('now', '-6 days')
                            {user_filter_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as datatable2
                    ON tempdatetable.date = datatable2.date
                    {other_event_str}
                ORDER BY date DESC;
            """
            
            
        else:
            # 如果提供了日期范围，使用提供的范围
            start_date, end_date = datetimerange
            sqlstr = f"""
                SELECT 
                        tempdatetable.date as date,
                        CASE
                            WHEN datatable1.count THEN datatable1.count
                            ELSE 0
                        END as {first_event},
                        CASE
                            WHEN datatable2.count THEN datatable2.count
                            ELSE 0
                        END as {second_event},
                        CASE 
                            WHEN datatable1.count
                            THEN CAST(ROUND((COALESCE(datatable2.count, 0) / CAST(datatable1.count AS FLOAT)), 4) * 100 AS TEXT) || '%'
                            ELSE '-'
                        END as retention_rate
                        {other_event_select_str}
                    FROM
                        (
                            WITH RECURSIVE date_range(date) AS (
                                SELECT date('{start_date}')
                                UNION ALL
                                SELECT date(date, '+1 day')
                                FROM date_range
                                WHERE date < date('{end_date}')
                            )
                            SELECT * FROM date_range
                        ) as tempdatetable
                LEFT JOIN
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date, 
                            eventKey, 
                            count(eventKey) as count
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{first_event}'
                            AND createtime BETWEEN '{start_date}' AND '{end_date}'
                            {user_filter_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as datatable1
                    ON tempdatetable.date = datatable1.date
                    LEFT JOIN  
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date, 
                            eventKey, 
                            count(eventKey) as count
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{second_event}'
                            AND createtime BETWEEN '{start_date}' AND '{end_date}'
                            {user_filter_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as datatable2
                    ON tempdatetable.date = datatable2.date
                    {other_event_str}
                ORDER BY date DESC;
            """

        
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
               
        if data[0]:
            column = [  
                        {
                            "dataIndex": item,
                            "title": item,
                            "renderOptions": {
                                "renderType": "ellipsis",
                            }
                            }
                        for item in data[0].keys()
                    ]
        else:
            column = []
        
        return column, data
    else:
        return [], []






# 注册retentionAnalysis的回调
def register_callbacks_retentionAnalysis(app):


    # 页面加载 加载options
    @app.callback(
        Output('first_event', 'options'),
        Output('second_event', 'options'),
        Output('other_event', 'options'),
        Output('user_filter', 'options'),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def retentionAnalysis_page(pathname):
        if pathname == '/retentionAnalysis':
            options = event_name_options_query()
            user_filter_options = user_filter_options_query()
            return options, options, options, user_filter_options
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update



    # 搜索按钮的回调
    @app.callback(
        Output('retentionAnalysis_table_table', 'columns'),
        Output('retentionAnalysis_table_table', 'data'),
        
        Input('retentionAnalysis-search', 'nClicks'),
        State('first_event', 'value'),
        State('second_event', 'value'),
        State('other_event', 'value'),
        State('user_filter', 'value'),
        State('user_filter_input', 'value'),
        State('datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def retentionAnalysis_search(nClicks, first_event, second_event, other_event, user_filter, user_filter_input, datetimerange):
        if nClicks and nClicks > 0:
            return retentionAnalysis_query(first_event, second_event, other_event, user_filter, user_filter_input, datetimerange)

        else:
            return dash.no_update



    # 重置按钮的回调
    @app.callback(
        Output('first_event', 'value'),
        Output('second_event', 'value'),
        Output('other_event', 'value'),
        Output('user_filter', 'value'),
        Output('user_filter_input', 'value'),
        Output('datetimerange', 'value'),
        
        Input('retentionAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def retentionAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None, None, None, None
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
        
        
        
        
        
        
        
        
        
             