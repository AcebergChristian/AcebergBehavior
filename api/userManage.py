import sqlite3
import dash
from dash import callback, Input, Output, State, html
import feffery_antd_components as fac
from common.sql import SQLiteClass
from common.tools import sha256_encrypt
from api.login import login, logout

from uuid import uuid4
from datetime import datetime




def users_query(condition="isdel='0' and role!='admin'"):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "users",
            "key, account, role, phone, creator, createtime, loginstatus",
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
            "users", columns="key, account, role, phone, creator, createtime, loginstatus"
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
    


def users_insert(data):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.select_data(
            "users",
            "account",
            condition="isdel='0'",
        )

    for item in existdata:
        if item["account"] == data["account"]:
            return False, "账号已存在"
        
    default_data = {
        "key": f"user_{str(uuid4())}",
        "creator": "admin",
        "createtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "loginstatus": "0",
        "isdel": "0",
    }
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.insert_data(
            "users", {**data, **default_data}
        )
    if res:
        return True, "新增成功"
    else:
        return False, "新增失败, 请检查"


def users_del(key):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.update_data(
            "users",
            {"isdel": "1"},
            condition=f"key='{key}'"
        )
        
    if existdata:
        return True, "删除成功"
    else:
        return False, "删除失败, 请检查"
    

def users_update(data):
    key = data["key"]
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.update_data("users", data, f"key='{key}'")
    if res:
        return True, "更新成功"
    else:
        return False, "更新失败, 请检查"




# 注册userManage的回调
def register_callbacks_userManage(app):

    @callback(
        Output('userManage-user_table', 'data'),
        Output('userManage-user_table', 'columns'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def userManage_mount(pathname):
        return users_query(), columns_query()
        
        
    # 点击展示新增用户的modal
    @callback(
        Output("userManage-adduser_modal", "visible", allow_duplicate=True),
        Input("userManage-adduser_btn", "nClicks"),
        prevent_initial_call=True,
    )
    def userManage_adduser_modalvisible(nClicks):
        if nClicks and nClicks > 0:
            return True
        else:
            dash.no_update


    # 新增用户
    @callback(
        Output("userManage-adduser_modal", "visible"),
        Output('userManage-message', 'children'),
        Output('userManage-user_table', 'data', allow_duplicate=True),

        Input('userManage-adduser_modal', 'okCounts'),
        [
            State('userManage-addform-user_account', 'value'),
            State('userManage-addform-user_password', 'value'),
            State('userManage-addform-user_phone', 'value'),
            State('userManage-addform-user_role', 'value'),
        ],
        prevent_initial_call=True,
    )
    def userManage_adduser_modal(okCounts, account, password, phone, role):
        if okCounts and okCounts > 0:
            data = {
                "account": account, 
                "password": sha256_encrypt(password), 
                "phone": phone,
                "role": role,
            }
            res = users_insert(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), users_query()
            else:
                return True, fac.AntdMessage(content=res[1], type='error'), users_query()

    # 查询条件
    @callback(
        Output('userManage-user_table', 'data', allow_duplicate=True),
        Input('userManage-search', 'nClicks'),
        State('userManage-search-form', 'values'),
        prevent_initial_call=True,
    )
    def userManage_search(nClicks, values):
        if nClicks and nClicks > 0 and values:
            # 从表单值中获取数据
            account = values.get('userManage-search-account', "")
            phone = values.get('userManage-search-phone', "")
            loginstatus = values.get('userManage-search-loginstatus', "")
            createtime = values.get('userManage-search-createtime', [])
                # 初始化条件列表
            conditions = []

            # 根据字段值构建查询条件
            if account:
                conditions.append(f"account like '%{account}%'")
            if phone:
                conditions.append(f"phone like '%{phone}%'")
            if loginstatus:
                conditions.append(f"loginstatus = {'1' if loginstatus == '登陆' else '0'} ")
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
                
            res = users_query(condition=query_str)

            return res
        else:
            return dash.no_update


    # 点击重置按钮，清空搜索表单
    @callback(
        Output('userManage-user_table', 'data', allow_duplicate=True),
        Output('userManage-search-form', 'values', allow_duplicate=True),
        Input('userManage-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def userManage_reset(nClicks):
        if nClicks and nClicks > 0:
            res = users_query()
            return res, {}
        else:
            return dash.no_update
        

    # 点击表格的更多的删除操作
    @callback(
        # Output('userManage-user_table', 'data', allow_duplicate=True),
        Output('userManage-del_modal', 'visible'),
        Output('userManage-del_modal', 'children'),
        Output('userManage-del_modal', 'title'),
        Input('userManage-user_table', 'nClicksDropdownItem'),
        State('userManage-user_table', 'recentlyClickedDropdownItemTitle'),
        State('userManage-user_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def userManage_table_dropdown_del(
        nClicksDropdownItem, recentlyClickedDropdownItemTitle, recentlyDropdownItemClickedRow):
        if recentlyClickedDropdownItemTitle == '删除':
            key = recentlyDropdownItemClickedRow['key']
            account = recentlyDropdownItemClickedRow['account']
            
            return True, fac.AntdText(f'是否确认删除名为 {account} 的用户？'), f"删除用户@{key}"
        else:
            return dash.no_update, dash.no_update, dash.no_update
        
    # 点击表格的更多的删除操作
    @callback(
        Output('userManage-user_table', 'data', allow_duplicate=True),
        Output('userManage-del_modal', 'visible', allow_duplicate=True),
        Output('userManage-message', 'children', allow_duplicate=True),
        Input('userManage-del_modal', 'okCounts'),
        Input('userManage-del_modal', 'title'),
        prevent_initial_call=True,
    )
    def userManage_table_dropdown_del_modalok(okCounts, title):
        if okCounts:
            key = title.split('@')[1]
            res = users_del(key)
            if res:
                return users_query() ,False, fac.AntdMessage(content=res[1], type='success')
            else:
                return users_query() ,False, fac.AntdMessage(content=res[1], type='error')
        else:
            return dash.no_update, dash.no_update, dash.no_update

    
    # 点击更多 编辑按钮
    @callback(
        Output("userManage-updateuser_modal", "visible", allow_duplicate=True),
        Output("userManage-updateuser_form", "values", allow_duplicate=True),
        Input('userManage-user_table', 'nClicksDropdownItem'),
        State('userManage-user_table', 'recentlyClickedDropdownItemTitle'),
        State('userManage-user_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def userManage_table_dropdown_update(nClicksDropdownItem,
                                  recentlyClickedDropdownItemTitle,
                                  recentlyDropdownItemClickedRow):

        if recentlyClickedDropdownItemTitle == '编辑':
            print('recentlyDropdownItemClickedRow', recentlyDropdownItemClickedRow)
            return True, recentlyDropdownItemClickedRow
        else:
            return dash.no_update, dash.no_update
    # 点击edit form 编辑按钮
    @callback(
        Output("userManage-updateuser_modal", "visible", allow_duplicate=True),
        Output('userManage-message', 'children', allow_duplicate=True),
        Output('userManage-user_table', 'data', allow_duplicate=True),

        Input('userManage-updateuser_modal', 'okCounts'),
        State('userManage-updateuser_form', 'values'),
        prevent_initial_call=True,
    )
    def userManage_table_dropdown_update_modalok(okCounts, values):
        if okCounts and okCounts > 0:
            data = {
                "key": values.get('key', ''),
                "account": values.get('account', ''), 
                "password": sha256_encrypt(values.get('password', '')), 
                "phone": values.get('phone', ''),
                "role": values.get('role', '')
            }
            res = users_update(data)
            
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), users_query()
            else:
                return False, fac.AntdMessage(content=res[1], type='error'), dash.no_update
        
        else:
            return dash.no_update, dash.no_update, dash.no_update