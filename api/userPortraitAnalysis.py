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
# def event_name_options_query():
#     with SQLiteClass("./acebergBehavior.db") as cursor:
#         data = cursor.select_data(
#             "eventManage",
#             "eventKey, eventName"
#         )
#     res = [{"label": item["eventName"], "value": item["eventKey"]} for item in data]
#     return res



# 用户筛选 options 查询
def user_meet_options_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        columns = cursor.select_columns(
            "realusers"
        )
    columns_filter = [{"label": item, "value": item} for item in columns if item not in ['key', 'account', 'password', 'role', 'isdel', 'creator', 'createtime']]
    return columns_filter



def userPortraitAnalysis_queryrealusers(user_meet, user_meet_input, datetimerange):
    
    datetimerange_str = ""
    if datetimerange:
        sessionstarttime, sessionendtime = datetimerange
        datetimerange_str = f"createtime BETWEEN '{sessionstarttime}' AND '{sessionendtime}'"
    else:
        datetimerange_str = '(1=1)'
        
    if user_meet and user_meet_input:
        
        sqlstr = f"""
            SELECT
                key,
                last_os,
                last_loc,
                sex,
                age
            FROM
                realusers
            WHERE
                {datetimerange_str}
                AND
                {user_meet} LIKE '%{user_meet_input}%'
        """
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
        # print(data)
    
                
        return data

    else:
        return []


# 查询event
def userPortraitAnalysis_queryevent(user_meet, user_meet_input, datetimerange):
    
    datetimerange_str = ""
    if datetimerange:
        starttime, endtime = datetimerange
        datetimerange_str = f"createtime BETWEEN '{starttime}' AND '{endtime}'"
    else:
        datetimerange_str = '(1=1)'
        
    if user_meet and user_meet_input:
        
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
        
        
        sqlstr = f"""
            SELECT
                strftime('%Y-%m-%d',createtime) AS date,
                SUM( CASE WHEN eventKey = 'app_run' THEN 1 ELSE 0 END ) AS app_run,
                SUM( CASE WHEN eventKey = 'payOrder' THEN 1 ELSE 0 END ) AS payOrder
            FROM
                event_to_user
            WHERE
                {datetimerange_str}
                AND
                (eventKey = 'app_run' OR eventKey = 'payOrder')
                {user_meet_str}
            GROUP BY
                strftime('%Y-%m-%d',createtime)
        """
        
        with SQLiteClass("./acebergBehavior.db") as cursor:
            data = cursor.custom_sql(
                sqlstr
            )
        # print(data)
    
                
        return data

    else:
        return []




# 注册userPortraitAnalysis的回调
def register_callbacks_userPortraitAnalysis(app):

    # 页面加载 加载options
    @callback(
        Output('userPortrait-user_meet', 'options', allow_duplicate=True),

        Input('url', 'pathname'),
        
        prevent_initial_call=True,
    )
    def userPortraitAnalysis_page(pathname):
        if pathname == '/userPortraitAnalysis':
            user_meet_options = user_meet_options_query()
            return user_meet_options
        else:
            return dash.no_update



    # 搜索按钮的回调
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_age'
            ),
            Output('userPortraitAnalysis_chart_age', 'children'),
        Input('userPortraitAnalysis_chart_age', 'data'),
    )
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_sex'
            ),
            Output('userPortraitAnalysis_chart_sex', 'children'),
        Input('userPortraitAnalysis_chart_sex', 'data'),
    )
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_os'
            ),
            Output('userPortraitAnalysis_chart_os', 'children'),
        Input('userPortraitAnalysis_chart_os', 'data'),
    )
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_loc'
            ),
            Output('userPortraitAnalysis_chart_loc', 'children'),
        Input('userPortraitAnalysis_chart_loc', 'data'),
    )
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_apprun'
            ),
            Output('userPortraitAnalysis_chart_apprun', 'children'),
        Input('userPortraitAnalysis_chart_apprun', 'data'),
    )
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userPortraitAnalysis_chart_pay'
            ),
            Output('userPortraitAnalysis_chart_pay', 'children'),
        Input('userPortraitAnalysis_chart_pay', 'data'),
    )
    @callback(
        Output('userPortraitAnalysis_chart_age', 'data'),
        Output('userPortraitAnalysis_chart_sex', 'data'),
        Output('userPortraitAnalysis_chart_os', 'data'),
        Output('userPortraitAnalysis_chart_loc', 'data'),
        Output('userPortraitAnalysis_chart_apprun', 'data'),
        Output('userPortraitAnalysis_chart_pay', 'data'),
        
        Output('userPortraitAnalysis_totalusernum', 'children'),
        Output('userPortraitAnalysis_targetusernum', 'children'),
        Output('userPortraitAnalysis_targetpercent', 'children'),
        
        
        Input('userPortraitAnalysis-search', 'nClicks'),
        State('userPortrait-user_meet', 'value'),
        State('userPortrait-user_meet_input', 'value'),
        State('userPortrait-datetimerange', 'value'),
        prevent_initial_call=True,
    )
    def userPortraitAnalysis_search(nClicks, user_meet, user_meet_input, datetimerange):
        if nClicks and nClicks > 0:
            try:
                res = userPortraitAnalysis_queryrealusers(user_meet, user_meet_input, datetimerange)
                eventres = userPortraitAnalysis_queryevent(user_meet, user_meet_input, datetimerange)
                
                # age data
                ageData_json = {}
                for item in res:
                    if item['age'] < 18:
                        ageData_json['0-18'] = ageData_json.get('0-18', 0) + 1
                    elif item['age'] >= 18 and item['age'] < 28:
                        ageData_json['18-28'] = ageData_json.get('18-28', 0) + 1
                    elif item['age'] >= 2825 and item['age'] < 38:
                        ageData_json['28-38'] = ageData_json.get('28-38', 0) + 1
                    elif item['age'] >= 38 and item['age'] < 50:
                        ageData_json['38-50'] = ageData_json.get('38-50', 0) + 1
                    elif item['age'] >= 50 and item['age'] < 65:
                        ageData_json['50-65'] = ageData_json.get('50-65', 0) + 1
                    else:
                        ageData_json['65以上'] = ageData_json.get('65以上', 0) + 1

                ageData = {
                    "x": list(ageData_json.keys()),
                    "y": list(ageData_json.values())
                }
                
                # sex data
                sex_male = 0
                sex_female = 0
                sex_unknown = 0
                for item in res:
                    sex_male += 1 if item['sex'] == '男' else 0
                    sex_female += 1 if item['sex'] == '女' else 0
                    sex_unknown += 1 if item['sex'] != '男' and item['sex'] != '女' else 0

                sexData = [
                    {"name": "男", "value": sex_male},
                    {"name": "女", "value": sex_female},
                    {"name": "未知", "value": sex_unknown}
                ]
                
                
                # os data
                osDataitem = {}
                for item in res:
                    if item['last_os'] not in osDataitem.keys():
                        osDataitem[item["last_os"]] = 1
                    else:
                        osDataitem[item["last_os"]] += 1

                osData = [{"name": item[0], "value": item[1]} for item in osDataitem.items()]
                
                
                # loc data
                locData_json = {}
                for item in res:
                    if item:
                        if item['last_loc'] in locData_json.keys():
                            locData_json[item["last_loc"]] += 1
                        else:
                            locData_json[item["last_loc"]] = 1
                    else:
                        if '未知' in locData_json.keys():
                            locData_json['未知'] += 1
                        else:
                            locData_json['未知'] = 1

                locData = {
                    "x": [item.split('-')[1] if item else '未知' for item in locData_json.keys()],
                    "y": list(locData_json.values())
                }
                    
                    
                # apprun 和 payOrder
                apprunData = {
                    "x": [item["date"] for item in eventres],
                    "y": [item["app_run"] for item in eventres]
                }
                payOrderData = {
                    "x": [item["date"] for item in eventres],
                    "y": [item["payOrder"] for item in eventres]
                }
                
                
                totalusernum = len(userPortraitAnalysis_queryrealusers('isdel', '0', ''))
                targetusernum = len(res)
                targetpercent = f"{round(targetusernum / totalusernum, 4) * 100}%"
    
                
                return ageData, sexData, osData, locData, apprunData, payOrderData, totalusernum, targetusernum, targetpercent
            
            except Exception as e:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
   
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update



    # 重置按钮的回调
    @callback(
        Output('userPortrait-user_meet', 'value', allow_duplicate=True),
        Output('userPortrait-user_meet_input', 'value', allow_duplicate=True),
        Output('userPortrait-datetimerange', 'value', allow_duplicate=True),
        
        Input('userPortraitAnalysis-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def userPortraitAnalysis_reset(nClicks):
        if nClicks and nClicks > 0:
            return None, None, None
        else:
            return dash.no_update, dash.no_update, dash.no_update
        
        
        
        
    # app.clientside_callback(
    #         ClientsideFunction(
    #             namespace='clientside',
    #             function_name='func_funnelAnalysis_chart_funnel'
    #         ),
    #         Output('funnelAnalysis_chart_funnel', 'children'),
    #     Input('funnelAnalysis_chart_funnel', 'columns'),
    #     Input('funnelAnalysis_chart_funnel', 'data'),
    # )
    # @callback(
    #     Output('funnelAnalysis_chart_funnel', 'columns'),
    #     Output('funnelAnalysis_chart_funnel', 'data'),
    #     Output('funnelAnalysis_chart_funnelTable_table', 'columns'),
    #     Output('funnelAnalysis_chart_funnelTable_table', 'data'),
    #     Input('funnelAnalysis-search', 'nClicks'),
    #     State('event_name_list', 'value'),
    #     State('event_datetime', 'value'),
    #     prevent_initial_call=True,
    # )
    # def funnelAnalysis_reset(nClicks, eventnamelist, datarange):