import dash
from dash import callback, Input, Output, State, html
import feffery_antd_components as fac
from common.sql import SQLiteClass

from uuid import uuid4
from datetime import datetime



def cron_query(condition="isdel='0'"):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "cronManage",
            "key, cronName, cronContent, cronDesc, creator, createtime",
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
            "cronManage", columns="key, cronName, cronContent,  cronDesc, creator, createtime"
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
    


def cron_insert(data):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.select_data(
            "cronManage",
            "cronName",
            condition="isdel='0'",
        )

    for item in existdata:
        if item["cronName"] == data["cronName"]:
            return False, "数据已存在"
        
    default_data = {
        "key": f"cron_{str(uuid4())}",
        "creator": data.get("creator", "admin"),
        "createtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "isdel": "0",
    }
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.insert_data(
            "cronManage", {**data, **default_data}
        )
    if res:
        return True, "新增成功"
    else:
        return False, "新增失败, 请检查"


def cron_del(key):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.update_data(
            "cronManage",
            {"isdel": "1"},
            condition=f"key='{key}'"
        )
        
    if existdata:
        return True, "删除成功"
    else:
        return False, "删除失败, 请检查"
    

def cron_update(data):
    key = data["key"]
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.update_data("cronManage", data, f"key='{key}'")
    if res:
        return True, "更新成功"
    else:
        return False, "更新失败, 请检查"




# 注册cronManage的回调
def register_callbacks_cronManage(app):

    @callback(
        Output('cronManage-cron_table', 'data'),
        Output('cronManage-cron_table', 'columns'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def cronManage_mount(pathname):
        return cron_query(), columns_query()
        
        
    # 点击展示新增用户的modal
    @callback(
        Output("cronManage-addcron_modal", "visible", allow_duplicate=True),
        Input("cronManage-addcron_btn", "nClicks"),
        prevent_initial_call=True,
    )
    def cronManage_addcron_modalvisible(nClicks):
        if nClicks and nClicks > 0:
            return True
        else:
            dash.no_update


    # 新增用户
    @callback(
        Output("cronManage-addcron_modal", "visible"),
        Output('cronManage-message', 'children'),
        Output('cronManage-cron_table', 'data', allow_duplicate=True),

        Input('cronManage-addcron_modal', 'okCounts'),
        [
            State('cronManage-addform-cronName', 'value'),
            State('cronManage-addform-cronContent', 'value'),
            State('cronManage-addform-cronDesc', 'value'),
            State('loginStatus', 'data'),
        ],
        prevent_initial_call=True,
    )
    def cronManage_addcron_modal(okCounts, cronName, cronContent, cronDesc, data):
        if okCounts and okCounts > 0:
            username = data['username']
            data = {
                "cronName": cronName, 
                "cronContent": cronContent, 
                "cronDesc": cronDesc,
                "creator": username,
            }
            res = cron_insert(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), cron_query()
            else:
                return True, fac.AntdMessage(content=res[1], type='error'), cron_query()

    # 查询条件
    @callback(
        Output('cronManage-cron_table', 'data', allow_duplicate=True),
        Input('cronManage-search', 'nClicks'),
        State('cronManage-search-form', 'values'),
        prevent_initial_call=True,
    )
    def cronManage_search(nClicks, values):
        if nClicks and nClicks > 0 and values:
            # 从表单值中获取数据
            cronName = values.get('cronManage-search-cronName', "")
            createtime = values.get('cronManage-search-createtime', [])
                # 初始化条件列表
            conditions = []

            # 根据字段值构建查询条件
            if cronName:
                conditions.append(f"cronName like '%{cronName}%'")
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
                
            res = cron_query(condition=query_str)

            return res
        else:
            return dash.no_update


    # 点击重置按钮，清空搜索表单
    @callback(
        Output('cronManage-cron_table', 'data', allow_duplicate=True),
        Output('cronManage-search-form', 'values', allow_duplicate=True),
        Input('cronManage-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def cronManage_reset(nClicks):
        if nClicks and nClicks > 0:
            res = cron_query()
            return res, {}
        else:
            return dash.no_update
        

    # 点击表格的更多的删除操作
    @callback(
        Output('cronManage-del_modal', 'visible'),
        Output('cronManage-del_modal', 'children'),
        Output('cronManage-del_modal', 'title'),
        Input('cronManage-cron_table', 'nClicksDropdownItem'),
        State('cronManage-cron_table', 'recentlyClickedDropdownItemTitle'),
        State('cronManage-cron_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def cronManage_table_dropdown_del(
        nClicksDropdownItem, recentlyClickedDropdownItemTitle, recentlyDropdownItemClickedRow):
        if recentlyClickedDropdownItemTitle == '删除':
            key = recentlyDropdownItemClickedRow['key']
            cronName = recentlyDropdownItemClickedRow['cronName']
            
            return True, fac.AntdText(f'是否确认删除名为 {cronName} 的数据？'), f"删除数据@{key}"
        else:
            return dash.no_update, dash.no_update, dash.no_update
    # 点击表格的更多的删除操作
    @callback(
        Output('cronManage-cron_table', 'data', allow_duplicate=True),
        Output('cronManage-del_modal', 'visible', allow_duplicate=True),
        Output('cronManage-message', 'children', allow_duplicate=True),
        Input('cronManage-del_modal', 'okCounts'),
        Input('cronManage-del_modal', 'title'),
        prevent_initial_call=True,
    )
    def cronManage_table_dropdown_del_modalok(okCounts, title):
        if okCounts:
            key = title.split('@')[1]
            res = cron_del(key)
            if res:
                return cron_query() ,False, fac.AntdMessage(content=res[1], type='success')
            else:
                return cron_query() ,False, fac.AntdMessage(content=res[1], type='error')
        else:
            return dash.no_update, dash.no_update, dash.no_update

    
    # 点击更多 编辑按钮
    @callback(
        Output("cronManage-updatecron_modal", "visible", allow_duplicate=True),
        Output("cronManage-updatecron_form", "values", allow_duplicate=True),
        Input('cronManage-cron_table', 'nClicksDropdownItem'),
        State('cronManage-cron_table', 'recentlyClickedDropdownItemTitle'),
        State('cronManage-cron_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def cronManage_table_dropdown_update(nClicksDropdownItem,
                                  recentlyClickedDropdownItemTitle,
                                  recentlyDropdownItemClickedRow):

        if recentlyClickedDropdownItemTitle == '编辑':
            return True, recentlyDropdownItemClickedRow
        else:
            return dash.no_update, dash.no_update
    # 点击edit form 编辑按钮
    @callback(
        Output("cronManage-updatecron_modal", "visible", allow_duplicate=True),
        Output('cronManage-message', 'children', allow_duplicate=True),
        Output('cronManage-cron_table', 'data', allow_duplicate=True),

        Input('cronManage-updatecron_modal', 'okCounts'),
        State('cronManage-updatecron_form', 'values'),
        prevent_initial_call=True,
    )
    def cronManage_table_dropdown_update_modalok(okCounts, values):
        if okCounts and okCounts > 0:
            data = {
                "key": values.get('key', ''),
                "cronName": values.get('cronName', ''),
                "cronContent": values.get('cronContent', ''),
                "cronDesc": values.get('cronDesc', '')
            }
            res = cron_update(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), cron_query()
            else:
                return False, fac.AntdMessage(content=res[1], type='error'), dash.no_update
        
        else:
            return dash.no_update, dash.no_update, dash.no_update