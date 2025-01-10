import dash
from dash import callback, Input, Output, State, html
import feffery_antd_components as fac
from common.sql import SQLiteClass

from uuid import uuid4
from datetime import datetime



def event_query(condition="isdel='0'"):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "eventManage",
            "key, eventKey, eventName, eventDesc, eventCategory, creator, createtime",
            condition=condition,
        )

    if data:
        res = [
            {
                **item,
                "operation": [
                    {
                        "title": "编辑",
                        "key": "edit",
                        "icon": "antd-edit",
                    },
                    {
                        "title": "删除",
                        "icon": "antd-delete",
                        "key": "delete",
                    }
                ],
            }
            for item in data
        ]
        
        return res
    else:
        return []


def columns_query():
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_columns(
            "eventManage", columns="key, eventKey, eventName, eventDesc, eventCategory, creator, createtime"
        )
    if data:
        res = [
            {
                "dataIndex": item,
                "title": item,
                "renderOptions": {"renderType": "ellipsis"},
            }
            for item in data
        ]
        
        operations = [
            {
                'title': '操作',
                'dataIndex': 'operation',
                'width': 120,
                'renderOptions': {
                    'renderType': 'dropdown',
                    'dropdownProps': {
                        'title': '更多',
                    },
                },
            }
        ]

        return res + operations
    else:
        return []
    


def event_insert(data):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.select_data(
            "eventManage",
            "eventKey",
            condition="isdel='0'",
        )

    for item in existdata:
        if item["eventKey"] == data["eventKey"]:
            return False, "数据已存在"
        
    default_data = {
        "key": f"event_{str(uuid4())}",
        "creator": data.get("creator", "admin"),
        "createtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "isdel": "0",
    }
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.insert_data(
            "eventManage", {**data, **default_data}
        )
    if res:
        return True, "新增成功"
    else:
        return False, "新增失败, 请检查"


def event_del(key):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.update_data(
            "eventManage",
            {"isdel": "1"},
            condition=f"key='{key}'"
        )
        
    if existdata:
        return True, "删除成功"
    else:
        return False, "删除失败, 请检查"
    

def event_update(data):
    key = data["key"]
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.update_data("eventManage", data, f"key='{key}'")
    if res:
        return True, "更新成功"
    else:
        return False, "更新失败, 请检查"




# 注册eventManage的回调
def register_callbacks_eventManage(app):

    @callback(
        Output('eventManage-event_table', 'data'),
        Output('eventManage-event_table', 'columns'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def eventManage_mount(pathname):
        return event_query(), columns_query()
        
        
    # 点击展示新增用户的modal
    @callback(
        Output("eventManage-addevent_modal", "visible", allow_duplicate=True),
        Input("eventManage-addevent_btn", "nClicks"),
        prevent_initial_call=True,
    )
    def eventManage_addevent_modalvisible(nClicks):
        if nClicks and nClicks > 0:
            return True
        else:
            dash.no_update


    # 新增用户
    @callback(
        Output("eventManage-addevent_modal", "visible"),
        Output('eventManage-message', 'children'),
        Output('eventManage-event_table', 'data', allow_duplicate=True),

        Input('eventManage-addevent_modal', 'okCounts'),
        [
            State('eventManage-addform-eventKey', 'value'),
            State('eventManage-addform-eventName', 'value'),
            State('eventManage-addform-eventDesc', 'value'),
            State('eventManage-addform-eventCategory', 'value'),
            State('loginStatus', 'data'),
        ],
        prevent_initial_call=True,
    )
    def eventManage_addevent_modal(okCounts, eventKey, eventName, eventDesc, eventCategory, data):
        if okCounts and okCounts > 0:
            username = data['username']
            data = {
                "eventKey": eventKey, 
                "eventName": eventName, 
                "eventDesc": eventDesc,
                "eventCategory": eventCategory,
                "creator": username,
            }
            res = event_insert(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), event_query()
            else:
                return True, fac.AntdMessage(content=res[1], type='error'), event_query()

    # 查询条件
    @callback(
        Output('eventManage-event_table', 'data', allow_duplicate=True),
        Input('eventManage-search', 'nClicks'),
        State('eventManage-search-form', 'values'),
        prevent_initial_call=True,
    )
    def eventManage_search(nClicks, values):
        if nClicks and nClicks > 0 and values:
            # 从表单值中获取数据
            eventName = values.get('eventManage-search-eventName', "")
            createtime = values.get('eventManage-search-createtime', [])
                # 初始化条件列表
            conditions = []

            # 根据字段值构建查询条件
            if eventName:
                conditions.append(f"eventName like '%{eventName}%'")
            # 假设 createtime 是一个日期范围列表，例如 ['2023-01-01', '2023-01-31']
            if createtime and len(createtime) == 2:
                start_date, end_date = createtime
                conditions.append(f"createtime between '{start_date}' and '{end_date}'")

            # 构建最终的查询字符串
            if conditions:
                condition_str = " and ".join(conditions) + " and isdel='0'"
                query_str = f" {condition_str}"
            else:
                query_str = "isdel='0'"
                
            res = event_query(condition=query_str)

            return res
        else:
            return dash.no_update


    # 点击重置按钮，清空搜索表单
    @callback(
        Output('eventManage-event_table', 'data', allow_duplicate=True),
        Output('eventManage-search-form', 'values', allow_duplicate=True),
        Input('eventManage-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def eventManage_reset(nClicks):
        if nClicks and nClicks > 0:
            res = event_query()
            return res, {}
        else:
            return dash.no_update
        

    # 点击表格的更多的删除操作
    @callback(
        Output('eventManage-del_modal', 'visible'),
        Output('eventManage-del_modal', 'children'),
        Output('eventManage-del_modal', 'title'),
        Input('eventManage-event_table', 'nClicksDropdownItem'),
        State('eventManage-event_table', 'recentlyClickedDropdownItemTitle'),
        State('eventManage-event_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def eventManage_table_dropdown_del(
        nClicksDropdownItem, recentlyClickedDropdownItemTitle, recentlyDropdownItemClickedRow):
        if recentlyClickedDropdownItemTitle == '删除':
            key = recentlyDropdownItemClickedRow['key']
            eventName = recentlyDropdownItemClickedRow['eventName']
            
            return True, fac.AntdText(f'是否确认删除名为 {eventName} 的数据？'), f"删除数据@{key}"
        else:
            return dash.no_update, dash.no_update, dash.no_update
    # 点击表格的更多的删除操作
    @callback(
        Output('eventManage-event_table', 'data', allow_duplicate=True),
        Output('eventManage-del_modal', 'visible', allow_duplicate=True),
        Output('eventManage-message', 'children', allow_duplicate=True),
        Input('eventManage-del_modal', 'okCounts'),
        Input('eventManage-del_modal', 'title'),
        prevent_initial_call=True,
    )
    def eventManage_table_dropdown_del_modalok(okCounts, title):
        if okCounts:
            key = title.split('@')[1]
            res = event_del(key)
            if res:
                return event_query() ,False, fac.AntdMessage(content=res[1], type='success')
            else:
                return event_query() ,False, fac.AntdMessage(content=res[1], type='error')
        else:
            return dash.no_update, dash.no_update, dash.no_update

    
    # 点击更多 编辑按钮
    @callback(
        Output("eventManage-updateevent_modal", "visible", allow_duplicate=True),
        Output("eventManage-updateevent_form", "values", allow_duplicate=True),
        Input('eventManage-event_table', 'nClicksDropdownItem'),
        State('eventManage-event_table', 'recentlyClickedDropdownItemTitle'),
        State('eventManage-event_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def eventManage_table_dropdown_update(nClicksDropdownItem,
                                  recentlyClickedDropdownItemTitle,
                                  recentlyDropdownItemClickedRow):

        if recentlyClickedDropdownItemTitle == '编辑':
            return True, recentlyDropdownItemClickedRow
        else:
            return dash.no_update, dash.no_update
    # 点击edit form 编辑按钮
    @callback(
        Output("eventManage-updateevent_modal", "visible", allow_duplicate=True),
        Output('eventManage-message', 'children', allow_duplicate=True),
        Output('eventManage-event_table', 'data', allow_duplicate=True),

        Input('eventManage-updateevent_modal', 'okCounts'),
        State('eventManage-updateevent_form', 'values'),
        prevent_initial_call=True,
    )
    def eventManage_table_dropdown_update_modalok(okCounts, values):
        if okCounts and okCounts > 0:
            data = {
                "key": values.get('key', ''),
                "eventKey": values.get('eventKey', ''),
                "eventName": values.get('eventName', ''),
                "eventDesc": values.get('eventDesc', ''),
                "eventCategory": values.get('eventCategory', '')
            }
            res = event_update(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), event_query()
            else:
                return False, fac.AntdMessage(content=res[1], type='error'), dash.no_update
        
        else:
            return dash.no_update, dash.no_update, dash.no_update