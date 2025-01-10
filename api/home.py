import dash
from dash import html, dcc, Input, Output, callback
from dash.dependencies import ClientsideFunction
import feffery_antd_components as fac

import random
import json

# 导入CHINAJSON 数据
import sys
from pathlib import Path
current_file_path = Path(__file__).resolve()
# 获取项目根目录的路径
project_root = current_file_path.parent.parent
# 将assets目录添加到sys.path
sys.path.insert(0, project_root)
# 现在可以导入map模块
from assets.materials.map import CHINAJSON



# 注册home的回调
def register_callbacks_home(app):

    # home_chart_PVline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_home_chart_PVline'
            ),
            Output('home_chart_PVline', 'children'),
            Input('home_chart_PVline', 'data'),
    )
    @callback(
        Output('home_chart_PVline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def home_chart_PVline(pathname):
        res = {
            'x': ['08-01', '08-02', '08-03', '08-04', '08-05', '08-06', '08-07'],
            'y': [ int(random.random()*20) for i in range(10)]
        }
        return res
    


    # home_chart_UVline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_home_chart_UVline'
            ),
            Output('home_chart_UVline', 'children'),
            Input('home_chart_UVline', 'data'),
    )
    @callback(
        Output('home_chart_UVline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def home_chart_UVline(pathname):
        res = {
            'x': ['08-01', '08-02', '08-03', '08-04', '08-05', '08-06', '08-07'],
            'y': [ int(random.random()*20) for i in range(10)]
        }
        return res
    
    

    # home_chart_UserGraph
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_home_chart_UserGraph'
            ),
            Output('home_chart_UserGraph', 'children'),
            Input('home_chart_UserGraph', 'data'),
            Input('home_chart_UserGraph', 'chinajson'),
    )
    @callback(
        Output('home_chart_UserGraph', 'data'),
        Output('home_chart_UserGraph', 'chinajson'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def home_chart_UserGraph(pathname):
        CHINAJSON_str = json.dumps(CHINAJSON)
        res = [
                { "name": "广东", "value": 12 },
                { "name": "浙江", "value": 2},
                { "name": "江苏", "value": 4 },
                { "name": "山东", "value": 4 },
                { "name": "四川", "value": 0 },
                { "name": "湖北", "value": 0 },
                { "name": "河南", "value": 0 },
                { "name": "河北", "value": 0 },
                { "name": "辽宁", "value": 0 },
                { "name": "云南", "value": 0 },
                { "name": "北京", "value": 0 },
                { "name": "安徽", "value": 0 },
                { "name": "上海", "value": 0 },
                { "name": "广西", "value": 0 },
                { "name": "福建", "value": 0 },
                { "name": "湖南", "value": 0 },
                { "name": "陕西", "value": 0 },
                { "name": "重庆", "value": 0 },
                { "name": "深圳", "value": 0 },
                { "name": "江西", "value": 0 },
                { "name": "山西", "value": 0 },
                { "name": "黑龙江", "value": 0 },
                { "name": "贵州", "value": 0 },
                { "name": "内蒙古", "value": 0 },
                { "name": "新疆", "value": 0 },
                { "name": "吉林", "value": 0 },
                { "name": "天津", "value": 0 },
                { "name": "甘肃", "value": 0 },
                { "name": "宁夏", "value": 0 },
                { "name": "海南", "value": 0 },
                { "name": "青海", "value": 0 },
                { "name": "西藏", "value": 0 },
                { "name": "台湾", "value": 0 },
              ];
        res_str = json.dumps(res, ensure_ascii=False)
        
        return res, CHINAJSON
    

    # home_chart_Genderpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_home_chart_Genderpie'
            ),
            Output('home_chart_Genderpie', 'children'),
            Input('home_chart_Genderpie', 'data'),
    )
    @callback(
        Output('home_chart_Genderpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def home_chart_Genderpie(pathname):
        res = [
            { 'value': 1048, 'name': '男(Male)' },
            { 'value': 735, 'name': '女(Female)' },
        ]
        return res
    
    # home_chart_Sourcepie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_home_chart_Sourcepie'
            ),
            Output('home_chart_Sourcepie', 'children'),
            Input('home_chart_Sourcepie', 'data'),
    )
    @callback(
        Output('home_chart_Sourcepie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def home_chart_Sourcepie(pathname):
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