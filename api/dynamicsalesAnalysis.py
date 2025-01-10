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



# 注册dynamicsalesAnalysis的回调
def register_callbacks_dynamicsalesAnalysis(app):

    # dynamicsalesAnalysis_chart_cancelorder
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_dynamicsalesAnalysis_chart_cancelorder'
            ),
            Output('dynamicsalesAnalysis_chart_cancelorder', 'children'),
            Input('dynamicsalesAnalysis_chart_cancelorder', 'data'),
    )
    @callback(
        Output('dynamicsalesAnalysis_chart_cancelorder', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def dynamicsalesAnalysis_chart_cancelorder(pathname):
        res = {
            'x': ['12-09', '12-10', '12-11', '12-12', '12-13', '12-14', '12-15'],
            'y': [ int(random.random()*20) for i in range(7)]
        }
        return res
    
    
    # dynamicsalesAnalysis_chart_gmv30
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_dynamicsalesAnalysis_chart_gmv30'
            ),
            Output('dynamicsalesAnalysis_chart_gmv30', 'children'),
            Input('dynamicsalesAnalysis_chart_gmv30', 'data'),
    )
    @callback(
        Output('dynamicsalesAnalysis_chart_gmv30', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def dynamicsalesAnalysis_chart_gmv30(pathname):
        res = {
            'x': ['11-19', '11-20', '11-21', '11-22', '11-23', '11-24', '11-25', '11-26', '11-27', '11-28', '11-29', '11-30', 
                  '12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07', '12-08', '12-09', '12-10', '12-11', '12-12', 
                  '12-13', '12-14', '12-15', '12-16', '12-17', '12-18', '12-19'],
            'y': [ int(random.random()*88888) for i in range(30)]
        }
        return res
    


    # dynamicsalesAnalysis_chart_gmvcontribute
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_dynamicsalesAnalysis_chart_gmvcontribute'
            ),
            Output('dynamicsalesAnalysis_chart_gmvcontribute', 'children'),
            Input('dynamicsalesAnalysis_chart_gmvcontribute', 'data'),
    )
    @callback(
        Output('dynamicsalesAnalysis_chart_gmvcontribute', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def dynamicsalesAnalysis_chart_gmvcontribute(pathname):
        # 各个终端系统
        data = ['MacOS', 'Windows', 'iOS', 'Android', 'Linux', '小程序']
        res = [{"name": item, "value": int(random.random()*9999)} for item in data]
        return res
    
    
    
    # dynamicsalesAnalysis_chart_salestrend
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_dynamicsalesAnalysis_chart_salestrend'
            ),
            Output('dynamicsalesAnalysis_chart_salestrend', 'children'),
            Input('dynamicsalesAnalysis_chart_salestrend', 'data'),
    )
    @callback(
        Output('dynamicsalesAnalysis_chart_salestrend', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def dynamicsalesAnalysis_chart_salestrend(pathname):
        date = ['2024-12-09', '2024-12-10', '2024-12-11', '2024-12-12', '2024-12-13', '2024-12-14', '2024-12-15', '2024-12-16', '2024-12-17']
        catory = ['服饰', '数码', '食品', '家居', '母婴', '运动', '图书', '玩具', '乐器']
        # 各类商品销售趋势
        res = {
            'x': date,
            'y': [ {"name":item, "data": [int(random.random()*999) for i in range(9)], "type": "line", "smooth":True} for item in catory]
        }
        return res
    
    
    # dynamicsalesAnalysis_chart_shoprate
    app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='func_dynamicsalesAnalysis_chart_shoprate'
            ),
            Output('dynamicsalesAnalysis_chart_shoprate', 'children'),
            Input('dynamicsalesAnalysis_chart_shoprate', 'data'),
    )
    @callback(
        Output('dynamicsalesAnalysis_chart_shoprate', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def dynamicsalesAnalysis_chart_shoprate(pathname):
        # 各个商铺占比
        data = ['店铺A', '店铺B', '店铺C', '店铺D', '店铺E', '店铺F', '店铺G', '店铺H', '店铺I']
        res = [{"name": item, "value": int(random.random()*9999)} for item in data]
        return res

    