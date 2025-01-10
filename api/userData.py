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



# 注册userData的回调
def register_callbacks_userData(app):

    # userData_chart_Agecutline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Agecutline'
            ),
            Output('userData_chart_Agecutline', 'children'),
            Input('userData_chart_Agecutline', 'data'),
    )
    @callback(
        Output('userData_chart_Agecutline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Agecutline(pathname):
        res = {
            'x': ['0-18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    

    # userData_chart_Vipline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Vipline'
            ),
            Output('userData_chart_Vipline', 'children'),
            Input('userData_chart_Vipline', 'data'),
    )
    @callback(
        Output('userData_chart_Vipline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Vipline(pathname):
        res = {
            'x': ['vip0', 'vip1', 'vip2', 'vip3', 'vip4', 'vip5', 'vip6'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    
      
    # userData_chart_Genderpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Genderpie'
            ),
            Output('userData_chart_Genderpie', 'children'),
            Input('userData_chart_Genderpie', 'data'),
    )
    @callback(
        Output('userData_chart_Genderpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Genderpie(pathname):
        res = [
            { 'value': 1048, 'name': '男(Male)' },
            { 'value': 735, 'name': '女(Female)' },
        ]
        return res
    
    # userData_chart_Sourcepie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Sourcepie'
            ),
            Output('userData_chart_Sourcepie', 'children'),
            Input('userData_chart_Sourcepie', 'data'),
    )
    @callback(
        Output('userData_chart_Sourcepie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Sourcepie(pathname):
        
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
    
    
    # userData_chart_Careerpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Careerpie'
            ),
            Output('userData_chart_Careerpie', 'children'),
            Input('userData_chart_Careerpie', 'data'),
    )
    @callback(
        Output('userData_chart_Careerpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Careerpie(pathname):
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
    
    
    # userData_chart_OSpie
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_OSpie'
            ),
            Output('userData_chart_OSpie', 'children'),
            Input('userData_chart_OSpie', 'data'),
    )
    @callback(
        Output('userData_chart_OSpie', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_OSpie(pathname):
        
        res = [
            { 'value': 9048, 'name': 'Windows' },
            { 'value': 2735, 'name': 'IOS' },
            { 'value': 3580, 'name': 'MacOS' },
            { 'value': 2484, 'name': 'Android' },
            { 'value': 6300, 'name': 'Linux' }
        ]
        return res
    


    # userData_chart_Activityline
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_Activityline'
            ),
            Output('userData_chart_Activityline', 'children'),
            Input('userData_chart_Activityline', 'data'),
    )
    @callback(
        Output('userData_chart_Activityline', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Activityline(pathname):
        res = {
            'x': ['202312', '202401', '202402', '202403', '202404', '202405', '202406', '202407',
            '202408', '202409', '202410', '202411'],
            'y': [ int(random.random()*200)+6 for i in range(12)]
        }
        return res
    
    
    # userData_chart_Pointstable
    @callback(
        Output('userData_chart_Pointstable_table', 'columns'),
        Output('userData_chart_Pointstable_table', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_Activityline(pathname):
        columns = [
            {
                "dataIndex": 'account',
                "title": 'account',
                "renderOptions": {"renderType": "ellipsis"},
            },
            {
                "dataIndex": 'sex',
                "title": 'sex',
                "renderOptions": {"renderType": "ellipsis"},
            },
            {
                "dataIndex": 'last_os',
                "title": 'last_os',
                "renderOptions": {"renderType": "ellipsis"},
            },
            {
                "dataIndex": 'status',
                "title": 'status',
                "renderOptions": {"renderType": "ellipsis"},
            },
            {
                "dataIndex": 'points',
                "title": 'points',
                "renderOptions": {"renderType": "ellipsis"},
            },

        ]
        data = [
            {
                "account": 'user1',
                "sex": '男',
                "last_os": 'Windows',
                "status": '活跃',
                "points": '100',
            },
            {
                "account": 'user2',
                "sex": '女',
                "last_os": 'MacOS',
                "status": '活跃',
                "points": '200',
            },
            {
                "account": 'user3',
                "sex": '男',
                "last_os": 'Linux',
                "status": '活跃',
                "points": '300',
            },
            {
                "account": 'user4',
                "sex": '女',
                "last_os": 'Windows',
                "status": '活跃',
                "points": '400',
            },
            {
                "account": 'user5',
                "sex": '男',
                "last_os": 'MacOS',
                "status": '活跃',
                "points": '500',
            },
            {
                "account": 'user6',
                "sex": '女',
                "last_os": 'Linux',
                "status": '活跃',
                "points": '600',
            },
            {
                "account": 'user7',
                "sex": '男',
                "last_os": 'Windows',
                "status": '活跃',
                "points": '700',
            },
            {
                "account": 'user8',
                "sex": '女',
                "last_os": 'MacOS',
                "status": '活跃',
                "points": '800',
            },
            {
                "account": 'user9',
                "sex": '男',
                "last_os": 'Linux',
                "status": '活跃',
                "points": '900',
            }
        ]
        return columns, sorted(data, key=lambda x: x['points'], reverse=True)
    
    
    # userData_chart_UserGraph
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_userData_chart_UserGraph'
            ),
            Output('userData_chart_UserGraph', 'children'),
            Input('userData_chart_UserGraph', 'data'),
            Input('userData_chart_UserGraph', 'chinajson'),
    )
    @callback(
        Output('userData_chart_UserGraph', 'data'),
        Output('userData_chart_UserGraph', 'chinajson'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userData_chart_UserGraph(pathname):
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
  