import dash
from dash import html, dcc, Input, Output, callback, State
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

from common.sql import SQLiteClass
import random
import json



def tagAnalysis_chart_Tagtable_query(tag_name, datatype, 
                            createmethod, status ,current,condition="isdel='0'"):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        columns = cursor.select_columns(
            "tagManage",
            "*"
        )
        if columns:
            res_columns = [
                {
                "dataIndex": 'key',
                "title": 'key',
                "renderOptions": {"renderType": "ellipsis"},
                }
            ]
            for item in columns:
                if item !="key":
                    res_columns.append({
                        "dataIndex": item,
                        "title": item,
                        "renderOptions": {"renderType": "ellipsis"},
                    })
        else:
            res_columns = []
        
        condition_str = ""
        if tag_name:
            condition_str= condition_str + f" and tag_name like '%{tag_name}%'"
        if datatype:
            condition_str = condition_str + f" and datatype = '{datatype}'"
        if createmethod:
            condition_str = condition_str + f" and createmethod = '{createmethod}'"
        if status:
            condition_str = condition_str + f" and status = '{status}'"
        
        data = cursor.select_data(
            "tagManage",
            "*",
            condition= condition + condition_str 
        )
        
        # total = cursor.select_data(
        #     "tagManage",
        #     "*",
        # )
        
            
        # pagination = {"current":current, "pageSize":10, "total":len(total)}

    return res_columns, data #, pagination



# 注册tagAnalysis的回调
def register_callbacks_tagAnalysis(app):


    # tagAnalysis_chart_Tagtable
    @app.callback(
        Output('tagAnalysis_chart_Tagtable_table', 'columns'),
        Output('tagAnalysis_chart_Tagtable_table', 'data'),
        # Output('tagAnalysis_chart_Tagtable_table', 'pagination'),
        Input('url', 'pathname'),
        Input('tagAnalysis_chart_Tagtable_table', 'pagination'),
        Input('tagAnalysis-search', 'nClicks'),

        State('tag_name', 'value'),
        State('tag_datatype', 'value'),
        State('tag_createmethod', 'value'),
        State('tag_status', 'value'),
        
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Tagtable(pathname, pagination,nClicks, tag_name, datatype, createmethod, status):
        if nClicks:
            return tagAnalysis_chart_Tagtable_query(tag_name, datatype, 
                                                createmethod, status, pagination['current'])
        else:
            return tagAnalysis_chart_Tagtable_query(tag_name, datatype, 
                                                createmethod, status, pagination['current'])
    
    

    # tagAnalysis_chart_Taggrouppie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Taggrouppie'
            ),
            Output('tagAnalysis_chart_Taggrouppie', 'children'),
            Input('tagAnalysis_chart_Taggrouppie', 'data')
    )
    @app.callback(
        Output('tagAnalysis_chart_Taggrouppie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Taggrouppie(pathname):
        res = [
            { 'value': 1048, 'name': '用户活跃度' },
            { 'value': 550, 'name': '用户粘性' },
            { 'value': 475, 'name': '用户价值' },
            { 'value': 300, 'name': '用户行为' },
            { 'value': 288, 'name': '用户属性' },
            { 'value': 268, 'name': '用户画像' },
            { 'value': 238, 'name': '自定义' },
        ]
        return res
    
    
    
    # tagAnalysis_chart_Importanttagcoverbar
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Importanttagcoverbar'
            ),
            Output('tagAnalysis_chart_Importanttagcoverbar', 'children'),
            Input('tagAnalysis_chart_Importanttagcoverbar', 'data'),
            Input('tagAnalysis_chart_Importanttagcoverbar', 'years'),
            Input('tagAnalysis_chart_Importanttagcoverbar', 'datatypenum'),
    )
    @callback(
        Output('tagAnalysis_chart_Importanttagcoverbar', 'data'),
        Output('tagAnalysis_chart_Importanttagcoverbar', 'years'),
        Output('tagAnalysis_chart_Importanttagcoverbar', 'datatypenum'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Importanttagcoverbar(pathname):
        data = [
            [
                "coverusercount",
                "Tag",
                "datetime"
            ],
            [815,"day_active",20241101],[1314, "last24hour_active",20241101],
            [314, "everyaveactive_time",20241101],[2314, "firstlogin_datetime",20241101],
            [1814, "lastlogintocurrent_time",20241101],
            
            [765,"day_active",20241102],[1214, "last24hour_active",20241102],
            [214, "everyaveactive_time",20241102],[2014, "firstlogin_datetime",20241102],
            [2114, "lastlogintocurrent_time",20241102],
            
            [705,"day_active",20241103],[1100, "last24hour_active",20241103],
            [174, "everyaveactive_time",20241103],[1614, "firstlogin_datetime",20241103],
            [514, "lastlogintocurrent_time",20241103],
            
            [645,"day_active",20241104],[914, "last24hour_active",20241104],
            [123, "everyaveactive_time",20241104],[614, "firstlogin_datetime",20241104],
            [2333, "lastlogintocurrent_time",20241104],
        ]
        years = ["datetime", 20241101, 20241102, 20241103, 20241104]
        datatypenum = 4
        return data, years, datatypenum




















    # tagAnalysis_chart_Agecutline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Agecutline'
            ),
            Output('tagAnalysis_chart_Agecutline', 'children'),
            Input('tagAnalysis_chart_Agecutline', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Agecutline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Agecutline(pathname):
        res = {
            'x': ['0-18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    

    # tagAnalysis_chart_Vipline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Vipline'
            ),
            Output('tagAnalysis_chart_Vipline', 'children'),
            Input('tagAnalysis_chart_Vipline', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Vipline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Vipline(pathname):
        res = {
            'x': ['vip0', 'vip1', 'vip2', 'vip3', 'vip4', 'vip5', 'vip6'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    
      
    # tagAnalysis_chart_Genderpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Genderpie'
            ),
            Output('tagAnalysis_chart_Genderpie', 'children'),
            Input('tagAnalysis_chart_Genderpie', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Genderpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Genderpie(pathname):
        res = [
            { 'value': 1048, 'name': '男(Male)' },
            { 'value': 735, 'name': '女(Female)' },
        ]
        return res
    
    # tagAnalysis_chart_Sourcepie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Sourcepie'
            ),
            Output('tagAnalysis_chart_Sourcepie', 'children'),
            Input('tagAnalysis_chart_Sourcepie', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Sourcepie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Sourcepie(pathname):
        
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
    
    
    # tagAnalysis_chart_Careerpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Careerpie'
            ),
            Output('tagAnalysis_chart_Careerpie', 'children'),
            Input('tagAnalysis_chart_Careerpie', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Careerpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Careerpie(pathname):
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
    
    
    # tagAnalysis_chart_OSpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_OSpie'
            ),
            Output('tagAnalysis_chart_OSpie', 'children'),
            Input('tagAnalysis_chart_OSpie', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_OSpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_OSpie(pathname):
        
        res = [
            { 'value': 9048, 'name': 'Windows' },
            { 'value': 2735, 'name': 'IOS' },
            { 'value': 3580, 'name': 'MacOS' },
            { 'value': 2484, 'name': 'Android' },
            { 'value': 6300, 'name': 'Linux' }
        ]
        return res
    


    # tagAnalysis_chart_Activityline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_tagAnalysis_chart_Activityline'
            ),
            Output('tagAnalysis_chart_Activityline', 'children'),
            Input('tagAnalysis_chart_Activityline', 'data'),
    )
    @app.callback(
        Output('tagAnalysis_chart_Activityline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagAnalysis_chart_Activityline(pathname):
        res = {
            'x': ['202312', '202401', '202402', '202403', '202404', '202405', '202406', '202407',
            '202408', '202409', '202410', '202411'],
            'y': [ int(random.random()*200)+6 for i in range(12)]
        }
        return res
    
    
    