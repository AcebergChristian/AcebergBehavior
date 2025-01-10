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
def user_meet_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        columns = cursor.select_columns(
            "realusers"
        )
    columns_filter = [{"label": item, "value": item} for item in columns if item not in ['key', 'account', 'password', 'role', 'isdel', 'creator', 'createtime']]
    return columns_filter



# 判断动态查询条件方法
def judge_dynamic_query(user_action, user_meet, user_meet_input, other_action, datetimerange):
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
            user_meet_str = f"AND (1 = 2)"
    
    
    other_action_select_str = "" # select 的动态
    other_action_str = "" # 左链接的字符串
    if other_action:
        other_action_select_str = f"""
        ,
            CASE
                WHEN other_action_table.other_action_0_3 THEN other_action_table.other_action_0_3
                ELSE 0
            END as other_action_0_3,
            CASE
                WHEN other_action_table.other_action_3_6 THEN other_action_table.other_action_3_6
                ELSE 0
            END as other_action_3_6,
            CASE
                WHEN other_action_table.other_action_6_10 THEN other_action_table.other_action_6_10
                ELSE 0
            END as other_action_6_10,
            CASE
                WHEN other_action_table.other_action_10_plus THEN other_action_table.other_action_10_plus
                ELSE 0
            END as other_action_10_plus
        """
    
        if not datetimerange:
            datetimerange_str = "AND createtime >= date('now', '-6 days')"
        else:
            start_date, end_date = datetimerange
            datetimerange_str = f"AND createtime BETWEEN '{start_date}' AND '{end_date}'"
        other_action_str = f"""
                        LEFT JOIN  
                (
                    SELECT 
                        strftime('%Y-%m-%d', createtime) as date,
                        COUNT(eventKey) as total_count, 
                        SUM(CASE WHEN eventKey = '{other_action}' AND event_count <= 3 THEN 1 ELSE 0 END) as other_action_0_3,
                        SUM(CASE WHEN eventKey = '{other_action}' AND event_count > 3 AND event_count <= 6 THEN 1 ELSE 0 END) as other_action_3_6,
                        SUM(CASE WHEN eventKey = '{other_action}' AND event_count > 6 AND event_count <= 10 THEN 1 ELSE 0 END) as other_action_6_10,
                        SUM(CASE WHEN eventKey = '{other_action}' AND event_count > 10 THEN 1 ELSE 0 END) as other_action_10_plus
                    FROM
                        (
                            SELECT
                                eventKey, 
                                COUNT(eventKey) as event_count,
                                createtime
                            FROM
                                event_to_user
                            WHERE
                                eventKey = '{other_action}'
                                {datetimerange_str}
                                {user_meet_str}
                            GROUP BY
                                eventKey, strftime('%Y-%m-%d', createtime)
                        ) as other_action_query
                    GROUP BY
                        date
                ) as other_action_table
                ON tempdatetable.date = other_action_table.date
        """

    
    # user_action 必选
    if user_action:
        # 如果没有提供日期范围，默认查询近7天
        if not datetimerange:
            sqlstr = f"""
                SELECT 
                    tempdatetable.date as date,
                    
                    CASE
                        WHEN total_user_num_table.total_user_num THEN total_user_num_table.total_user_num
                        ELSE 0
                    END as total_user_num,
                    
                    CASE
                        WHEN user_action_table.user_num_0_3 THEN user_action_table.user_num_0_3
                        ELSE 0
                    END as user_num_0_3,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_0_3, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_0_3,
                    
                    CASE
                        WHEN user_action_table.user_num_3_6 THEN user_action_table.user_num_3_6
                        ELSE 0
                    END as user_num_3_6,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_3_6, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_3_6,
                    
                    CASE
                        WHEN user_action_table.user_num_6_10 THEN user_action_table.user_num_6_10
                        ELSE 0
                    END as user_num_6_10,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_6_10, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_6_10,
                    
                    CASE
                        WHEN user_action_table.user_num_10_plus THEN user_action_table.user_num_10_plus
                        ELSE 0
                    END as user_num_10_plus,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_10_plus, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_10_plus
                    {other_action_select_str}
                    
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
                            COUNT(userKey) as total_user_num
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{user_action}'
                            AND createtime >= date('now', '-6 days')
                            {user_meet_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as total_user_num_table
                    ON tempdatetable.date = total_user_num_table.date
                    
                    LEFT JOIN  
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date,
                            COUNT(eventKey) as total_count, 
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count <= 3 THEN 1 ELSE 0 END) as user_num_0_3,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 3 AND event_count <= 6 THEN 1 ELSE 0 END) as user_num_3_6,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 6 AND event_count <= 10 THEN 1 ELSE 0 END) as user_num_6_10,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 10 THEN 1 ELSE 0 END) as user_num_10_plus
                        FROM
                            (
                                SELECT
                                    eventKey, 
                                    COUNT(eventKey) as event_count,
                                    createtime
                                FROM
                                    event_to_user
                                WHERE
                                    eventKey = '{user_action}'
                                    AND createtime >= date('now', '-6 days')
                                    {user_meet_str}
                                GROUP BY
                                    strftime('%Y-%m-%d', createtime)
                            ) as user_event_counts
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as user_action_table
                    ON tempdatetable.date = user_action_table.date
                    
                    
                    {other_action_str}
                ORDER BY date DESC;
            """
        
        else:
            # 如果提供了日期范围，使用提供的范围
            start_date, end_date = datetimerange
            sqlstr = f"""
                SELECT 
                    tempdatetable.date as date,
                    
                    CASE
                        WHEN total_user_num_table.total_user_num THEN total_user_num_table.total_user_num
                        ELSE 0
                    END as total_user_num,
                    
                    CASE
                        WHEN user_action_table.user_num_0_3 THEN user_action_table.user_num_0_3
                        ELSE 0
                    END as user_num_0_3,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_0_3, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_0_3,
                    
                    CASE
                        WHEN user_action_table.user_num_3_6 THEN user_action_table.user_num_3_6
                        ELSE 0
                    END as user_num_3_6,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_3_6, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_3_6,
                    
                    CASE
                        WHEN user_action_table.user_num_6_10 THEN user_action_table.user_num_6_10
                        ELSE 0
                    END as user_num_6_10,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_6_10, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_6_10,
                    
                    CASE
                        WHEN user_action_table.user_num_10_plus THEN user_action_table.user_num_10_plus
                        ELSE 0
                    END as user_num_10_plus,
                    CASE 
                        WHEN total_user_num_table.total_user_num
                        THEN CAST(ROUND((COALESCE(user_action_table.user_num_10_plus, 0) / CAST(total_user_num_table.total_user_num AS FLOAT)), 4) * 100 AS TEXT) || '%'
                        ELSE '-'
                    END as rate_10_plus
                    {other_action_select_str}
                    
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
                            COUNT(userKey) as total_user_num
                        FROM
                            event_to_user
                        WHERE
                            eventKey = '{user_action}'
                            AND createtime BETWEEN '{start_date}' AND '{end_date}'
                            {user_meet_str}
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as total_user_num_table
                    ON tempdatetable.date = total_user_num_table.date
                    
                    LEFT JOIN  
                    (
                        SELECT 
                            strftime('%Y-%m-%d', createtime) as date,
                            COUNT(eventKey) as total_count, 
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count <= 3 THEN 1 ELSE 0 END) as user_num_0_3,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 3 AND event_count <= 6 THEN 1 ELSE 0 END) as user_num_3_6,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 6 AND event_count <= 10 THEN 1 ELSE 0 END) as user_num_6_10,
                            SUM(CASE WHEN eventKey = '{user_action}' AND event_count > 10 THEN 1 ELSE 0 END) as user_num_10_plus
                        FROM
                            (
                                SELECT
                                    eventKey, 
                                    COUNT(eventKey) as event_count,
                                    createtime
                                FROM
                                    event_to_user
                                WHERE
                                    eventKey = '{user_action}'
                                    AND createtime BETWEEN '{start_date}' AND '{end_date}'
                                    {user_meet_str}
                                GROUP BY
                                    strftime('%Y-%m-%d', createtime)
                            ) as user_event_counts
                        GROUP BY
                            strftime('%Y-%m-%d', createtime)
                    ) as user_action_table
                    ON tempdatetable.date = user_action_table.date
                    
                    
                    {other_action_str}
                ORDER BY date DESC;
            """   
        return sqlstr
    
    else:
        return ""



# start_date, end_date = datetimerange
# AND createtime BETWEEN '{start_date}' AND '{end_date}'                            
# 搜索后的查询方法
def distributionAnalysis_query(user_action, user_meet, user_meet_input, other_action, datetimerange):
    sqlstr = judge_dynamic_query(user_action, user_meet, user_meet_input, other_action, datetimerange)
    
    if sqlstr:
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
    else:
        data = []
        
               
    column = [
        {
            'title': 'date',
            'dataIndex': 'date'
        },
        {
            'title': '总人数',
            'dataIndex': 'total_user_num'
        },
        
        {
            'title': '人数',
            'dataIndex': 'user_num_0_3',
            'group': ['0次 ~ 3 次(不含 3 次)'],
        },
        {
            'title': '占比',
            'dataIndex': 'rate_0_3',
            'group': [ '0次 ~ 3 次(不含 3 次)'],
        },
        {
            'title': '其他行为',
            'dataIndex': 'other_action_0_3',
            'group': [ '0次 ~ 3 次(不含 3 次)'],
        },
        
        {
            'title': '人数',
            'dataIndex': 'user_num_3_6',
            'group': ['3次 ~ 6 次(不含 6 次)'],
        },
        {
            'title': '占比',
            'dataIndex': 'rate_3_6',
            'group': [ '3次 ~ 6 次(不含 6 次)'],
        },
        {
            'title': '其他行为',
            'dataIndex': 'other_action_3_6',
            'group': [ '3次 ~ 6 次(不含 6 次)'],
        },
        
        {
            'title': '人数',
            'dataIndex': 'user_num_6_10',
            'group': ['6次 ~ 10 次(不含 10 次)'],
        },
        {
            'title': '占比',
            'dataIndex': 'rate_6_10',
            'group': [ '6次 ~ 10 次(不含 10 次)'],
        },
        {
            'title': '其他行为',
            'dataIndex': 'other_action_6_10',
            'group': [ '6次 ~ 10 次(不含 10 次)'],
        },
        
        {
            'title': '人数',
            'dataIndex': 'user_num_10_plus',
            'group': ['10次以上'],
        },
        {
            'title': '占比',
            'dataIndex': 'rate_10_plus',
            'group': [ '10次以上'],
        },
        {
            'title': '其他行为',
            'dataIndex': 'other_action_10_plus',
            'group': [ '10次以上'],
        },
        
    ]
        
    return column, data







# 注册distributionAnalysis的回调
def register_callbacks_distributionAnalysis(app):

    # 页面加载 加载options
    @app.callback(
        Output('user_action', 'options', allow_duplicate=True),
        Output('other_action', 'options', allow_duplicate=True),
        Output('user_meet', 'options', allow_duplicate=True),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def distributionAnalysis_page(pathname):
        if pathname == '/distributionAnalysis':
            options = event_name_options_query()
            user_meet_options = user_meet_options_query()
            return options, options, user_meet_options
        else:
            return dash.no_update, dash.no_update, dash.no_update



    # 搜索按钮的回调
    @app.callback(
        Output('distributionAnalysis_table_table', 'columns'),
        Output('distributionAnalysis_table_table', 'data'),
        
        Input('distributionAnalysis-search', 'nClicks'),
        State('user_action', 'value'),
        State('user_meet', 'value'),
        State('user_meet_input', 'value'),
        State('other_action', 'value'),
        State('datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def distributionAnalysis_search(nClicks, user_action, user_meet, user_meet_input, other_action, datetimerange):
        if nClicks and nClicks > 0:
            return distributionAnalysis_query(user_action, user_meet, user_meet_input, other_action, datetimerange)

        else:
            return dash.no_update, dash.no_update




    # 重置按钮的回调
    @app.callback(
        Output('user_action', 'value', allow_duplicate=True),
        Output('user_meet', 'value', allow_duplicate=True),
        Output('user_meet_input', 'value', allow_duplicate=True),
        Output('other_action', 'value', allow_duplicate=True),
        Output('datetimerange', 'value', allow_duplicate=True),
        
        Input('distributionAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def distributionAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None, None, None
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        
        
        
        