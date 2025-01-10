import sqlite3
import dash
from dash import callback, Input, Output, State, html
from dash.dependencies import ALL
import feffery_antd_components as fac
from common.sql import SQLiteClass
from common.tools import sha256_encrypt
from api.login import login, logout

from uuid import uuid4
from datetime import datetime, timedelta
import time
import random
import json


# 事件查询接口
def event_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "eventManage",
            "eventKey, eventName"
        )
    return data


# 模拟数据插入 event_to_user 表
def simulate_data_insert(eventKey, eventName):
    key = str(uuid4())
    userlist = (("user_admin", "admin"),
                ("user_16be4b20-135e-4b4d-bb7f-7d787577bfff","test"),
                ("user_afaa9a87-3a81-4294-bc27-25776f403701", "user"),
                ("user_cbdc22f8-3da5-4d10-bc06-e62c32014ea0","account_0"),
                ("user_f9386ddc-61d1-4bed-b238-23b796ca30c7","account_1"),
                ("user_8efb04d0-ed33-4c58-8f09-16999c8a0714", "account_2"),
                ("user_978f19b4-7267-44bf-b30e-24764eb8dceb", "account_3"),
                ("user_4356e2f3-5b1d-4ddf-92cb-9612a6bba58b", "account_4"),
                ("user_a244fcbd-1aca-45d7-8d5e-1be2e3f26a43", "account_5"),
                ("user_c705f948-afcb-4cfd-af2a-97c55e6e9806", "account_6"),
                ("user_980b5bab-3e87-4639-aa82-69cf5e50d5aa", "account_7"),
                ("user_8f22062e-dcea-41e4-89fe-af0f33182db2", "account_8"),
                ("user_e246c5b7-a6be-4850-80c9-365ab1eba817", "account_9")
            )

    isdel = 0
    createtor = "admin"
    random_days = random.randint(0, 199)  # 随机增加0到10天
    createtime = (datetime.now() + timedelta(days=random_days)).strftime('%Y-%m-%d %H:%M:%S')

    itemdata = {
        "key": key,
        "eventKey": eventKey,
        "eventName": eventName,
        "userKey": random.choice(userlist)[0],
        "userAccount": random.choice(userlist)[1],
        "isdel": isdel,
        "creator": createtor,
        "createtime": createtime
    }
    
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.insert_data(
            "event_to_user",
            itemdata
        )
    if data:
        return "success"
    else:
        return "error"




# 注册SimulateAction的回调
def register_callbacks_simulateAction(app):

    @app.callback(
        Output('simulateAction-container', 'children'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def simulateAction_mount(pathname):
        eventdata = event_query()
        colors = [
            "#FFB6C1",  # Light Pink
            "#ADD8E6",  # Light Blue
            "#90EE90",  # Light Green
            "#FFDAB9",  # Peach Puff
            "#E6E6FA",  # Lavender
            "#FFFACD",  # Lemon Chiffon
            "#D3D3D3",  # Light Gray
            "#F0E68C",  # Khaki
            "#E0FFFF",  # Light Cyan
            "#FAFAD2"   # Light Goldenrod Yellow
        ]

        return [
            html.Div(
                [
                    html.Span(item['eventKey']),
                    html.Span(item['eventName'])
                ],
                className="simulateAction_box",
                id={"type": "simulateAction_box", "index": f"{item['eventKey']}@{item['eventName']}"},
                style={
                    "width": 120,
                    "height": 120,
                    "backgroundColor": random.choice(colors),
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": 6,
                    "alignItems": "center",
                    "justifyContent": "center",
                    "color": "#333333",
                    "fontSize": 12,
                    "borderRadius": 6,
                    "cursor": "pointer",
                    "overflow": "hidden"
                }
            ) for item in eventdata
        ]
        


    # div 点击message
    @app.callback(
        Output('simulateAction-message', 'children'),
        [Input({'type': 'simulateAction_box', 'index': dash.dependencies.ALL}, 'n_clicks')],
        prevent_initial_call=True,
    )
    def simulateAction_message(n_clicks):
        ctx = dash.callback_context

        if not ctx.triggered:
            return dash.no_update

        # 获取触发回调的组件的id 里的 index
        triggered_id_arr = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index'].split('@')
        
        actionKey = triggered_id_arr[0]
        actionName = triggered_id_arr[1]
        
        
        # for i in range(1099):
        #     time.sleep(0.19)
        #     item = random.choice(event_query())
        #     res = simulate_data_insert(item["eventKey"], item["eventName"])
    
        #     print(f"actionKey:{item['eventKey']}")
        #     # 将 return 移到循环外
        #     message_content = f"模拟事件{item['eventKey']} ---> {res}"
        #     message_type = f"{res}"
        
        # return fac.AntdMessage(content=message_content, type=message_type)


        if any(n_clicks):
            res = simulate_data_insert(actionKey, actionKey)
            print(f"actionKey:{actionKey}")
            return fac.AntdMessage(content=f"模拟事件{actionKey} ---> {res}", type=f"{res}")
        else:
            return dash.no_update
        
        
        
    # 点击自动运行
    @app.callback(
        Output('simulateAction-message', 'children', allow_duplicate=True),
        Input('simulateAction-autorun', 'nClicks'),
        State('simulateAction-times', 'value'),
        prevent_initial_call=True,
    )
    def simulateAction_autorun(nClicks, value):
        if nClicks:
            for i in range(value):
                time.sleep(0.19)
                item = random.choice(event_query())
                simulate_data_insert(item["eventKey"], item["eventName"])
                print(f"第{i}个模拟行为 ------> actionKey:{item['eventKey']}")
                
            # 在每次循环中返回消息
            return fac.AntdMessage(content="自动运行完成", type="success")
        
        else:
            return dash.no_update