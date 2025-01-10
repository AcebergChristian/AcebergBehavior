import dash
from dash import callback, Input, Output, State, html
import feffery_antd_components as fac
from common.sql import SQLiteClass

from uuid import uuid4
from datetime import datetime



def tag_query(condition="isdel='0'"):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.select_data(
            "tagManage",
            "key, tag_key, tag_name, value, togroup, datatype, coverusercount, status, createmethod, creator, createtime",
            condition=condition,
        )

    if data:
        column = [{
                "dataIndex": item,
                "title": item,
                "renderOptions": {"renderType": "ellipsis"},
            } for item in data[0].keys()] + [
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
                        "title": "详情",
                        "icon": "antd-info-circle",
                        "key": "info",
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
        
        
        return column, res
    else:
        return [], []
    


def tag_insert(data):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.select_data(
            "tagManage",
            "tag_key",
            condition="isdel='0'",
        )

    for item in existdata:
        if item["tag_key"] == data["tag_key"]:
            return False, "数据已存在"
        
    default_data = {
        "key": f"tag_{str(uuid4())}",
        "creator": data.get("creator", "admin"),
        "createtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "isdel": "0",
    }
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.insert_data(
            "tagManage", {**data, **default_data}
        )
    if res:
        return True, "新增成功"
    else:
        return False, "新增失败, 请检查"


def tag_del(key):
    with SQLiteClass("./acebergBehavior.db") as cursor:
        existdata = cursor.update_data(
            "tagManage",
            {"isdel": "1"},
            condition=f"key='{key}'"
        )
        
    if existdata:
        return True, "删除成功"
    else:
        return False, "删除失败, 请检查"
    

def tag_update(data):
    key = data["key"]
    with SQLiteClass("./acebergBehavior.db") as cursor:
        res = cursor.update_data("tagManage", data, f"key='{key}'")
    if res:
        return True, "更新成功"
    else:
        return False, "更新失败, 请检查"


def tag_info(data):
    try:
        tag_key = data.get("tag_key", "")
        
        if tag_key == "day_active":
            sqlstr= f"""
                SELECT
                    strftime('%Y-%m-%d', createtime) as x,
                    COUNT(eventKey) as {tag_key}
                FROM
                    event_to_user
                WHERE 
                    eventKey='app_run'
                    AND
                    createtime BETWEEN date('now', '-7 days') and  date('now')
                GROUP BY
                strftime('%Y-%m-%d', createtime)
            """
        elif tag_key == "week_active":
            sqlstr= f"""
                SELECT
                    strftime('%Y-%W', createtime) as x,
                    COUNT(eventKey) as {tag_key}
                FROM
                    event_to_user
                WHERE 
                    eventKey='app_run'
                    AND
                    createtime BETWEEN date('now', '-30 days') and  date('now')
                GROUP BY
                strftime('%Y-%W', createtime)
            """
        
        if sqlstr:
            with SQLiteClass("./acebergBehavior.db") as cursor:
                data = cursor.custom_sql(sqlstr)
            
            print("data=======>", data)
            if data:
                res = ", ".join([ f"{item['x']} : {item[f'{tag_key}']}" for item in data ])
            else:
                res = ""
            return res
        else:
            return []
    
    except Exception as e:
        print("tag_info error:", e)
        return []
    



# 注册tagManage的回调
def register_callbacks_tagManage(app):

    @callback(
        Output('tagManage-tag_table', 'columns'),
        Output('tagManage-tag_table', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def tagManage_mount(pathname):
        return tag_query()
        
        
    # 点击展示新增用户的modal
    @callback(
        Output("tagManage-addtag_modal", "visible", allow_duplicate=True),
        Input("tagManage-addtag_btn", "nClicks"),
        prevent_initial_call=True,
    )
    def tagManage_addtag_modalvisible(nClicks):
        if nClicks and nClicks > 0:
            return True
        else:
            dash.no_update


    # 新增用户
    @callback(
        Output("tagManage-addtag_modal", "visible"),
        Output('tagManage-message', 'children'),
        Output('tagManage-tag_table', 'columns', allow_duplicate=True),
        Output('tagManage-tag_table', 'data', allow_duplicate=True),

        Input('tagManage-addtag_modal', 'okCounts'),
        [
            State('tagManage-addform-tag_key', 'value'),
            State('tagManage-addform-tag_name', 'value'),
            State('tagManage-addform-togroup', 'value'),
            State('tagManage-addform-datatype', 'value'),
            State('tagManage-addform-createmethod', 'value'),
            State('tagManage-addform-status', 'value'),
            State('loginStatus', 'data'),
        ],
        prevent_initial_call=True,
    )
    def tagManage_addtag_modal(okCounts, tag_key, tag_name, togroup, datatype, createmethod, status, loginStatus):
        if okCounts and okCounts > 0:
            username = loginStatus['username']
            data = {
                "tag_key": tag_key, 
                "tag_name": tag_name, 
                "togroup": togroup,
                "datatype": datatype,
                "createmethod":createmethod,
                "status":status,
                "creator": username,
            }
            res = tag_insert(data)
            
            
            column, data = tag_query()
            if res[0]:
                return False, fac.AntdMessage(content=res[1], type='success'), column, data
            else:
                return True, fac.AntdMessage(content=res[1], type='error'), column, data

    # 查询条件
    @callback(
        Output('tagManage-tag_table', 'columns', allow_duplicate=True),
        Output('tagManage-tag_table', 'data', allow_duplicate=True),
        Input('tagManage-search', 'nClicks'),
        State('tagManage-search-form', 'values'),
        prevent_initial_call=True,
    )
    def tagManage_search(nClicks, values):
        if nClicks and nClicks > 0 and values:
            # 从表单值中获取数据
            eventName = values.get('tagManage-search-tagName', "")
            createtime = values.get('tagManage-search-createtime', [])
                # 初始化条件列表
            conditions = []

            # 根据字段值构建查询条件
            if eventName:
                conditions.append(f"tag_name like '%{eventName}%'")
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
                
            res = tag_query(condition=query_str)

            return res
        else:
            return dash.no_update, dash.no_update


    # 点击重置按钮，清空搜索表单
    @callback(
        Output('tagManage-tag_table', 'columns', allow_duplicate=True),
        Output('tagManage-tag_table', 'data', allow_duplicate=True),
        Output('tagManage-search-form', 'values', allow_duplicate=True),
        
        Input('tagManage-reset', 'nClicks'),
        prevent_initial_call=True,
    )
    def tagManage_reset(nClicks):
        if nClicks and nClicks > 0:
            column, data = tag_query()
            return column, data, {}
        else:
            return dash.no_update, dash.no_update, dash.no_update
        

    # 点击表格的更多的删除操作
    @callback(
        Output('tagManage-del_modal', 'visible'),
        Output('tagManage-del_modal', 'children'),
        Output('tagManage-del_modal', 'title'),
        Input('tagManage-tag_table', 'nClicksDropdownItem'),
        State('tagManage-tag_table', 'recentlyClickedDropdownItemTitle'),
        State('tagManage-tag_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def tagManage_table_dropdown_del(
        nClicksDropdownItem, recentlyClickedDropdownItemTitle, recentlyDropdownItemClickedRow):
        if recentlyClickedDropdownItemTitle == '删除':
            key = recentlyDropdownItemClickedRow['key']
            tag_key = recentlyDropdownItemClickedRow['tag_key']
            
            return True, fac.AntdText(f'是否确认删除名为 {tag_key} 的数据？'), f"删除数据@{key}"
        else:
            return dash.no_update, dash.no_update, dash.no_update
    # 点击表格的更多的删除操作
    @callback(
        Output('tagManage-tag_table', 'columns', allow_duplicate=True),
        Output('tagManage-tag_table', 'data', allow_duplicate=True),
        Output('tagManage-del_modal', 'visible', allow_duplicate=True),
        Output('tagManage-message', 'children', allow_duplicate=True),
        Input('tagManage-del_modal', 'okCounts'),
        Input('tagManage-del_modal', 'title'),
        prevent_initial_call=True,
    )
    def tagManage_table_dropdown_del_modalok(okCounts, title):
        if okCounts:
            key = title.split('@')[1]
            res = tag_del(key)
            column, data = tag_query()
            if res:
                return column, data ,False, fac.AntdMessage(content=res[1], type='success')
            else:
                return column, data ,False, fac.AntdMessage(content=res[1], type='error')
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    
    # 点击更多 编辑按钮
    @callback(
        Output("tagManage-updatetag_modal", "title", allow_duplicate=True),
        Output("tagManage-updatetag_modal", "visible", allow_duplicate=True),
        Output("tagManage-updatetag_form", "values", allow_duplicate=True),
        Input('tagManage-tag_table', 'nClicksDropdownItem'),
        State('tagManage-tag_table', 'recentlyClickedDropdownItemTitle'),
        State('tagManage-tag_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def tagManage_table_dropdown_update(nClicksDropdownItem,
                                  recentlyClickedDropdownItemTitle,
                                  recentlyDropdownItemClickedRow):
        if recentlyClickedDropdownItemTitle == '编辑':
            return f"编辑@{recentlyDropdownItemClickedRow['key']}", True, recentlyDropdownItemClickedRow
        else:
            return dash.no_update, dash.no_update, dash.no_update
    # 点击edit form 编辑按钮
    @callback(
        Output("tagManage-updatetag_modal", "visible", allow_duplicate=True),
        Output('tagManage-message', 'children', allow_duplicate=True),
        Output('tagManage-tag_table', 'columns', allow_duplicate=True),
        Output('tagManage-tag_table', 'data', allow_duplicate=True),

        Input('tagManage-updatetag_modal', 'okCounts'),
        State('tagManage-updatetag_form', 'values'),
        prevent_initial_call=True,
    )
    def tagManage_table_dropdown_update_modalok(okCounts, values):
        if okCounts and okCounts > 0:
            datajson = {}
            for k,v in values.items():
                if k != 'operation':
                    datajson[k]=v
            res = tag_update(datajson)
            
            if res[0]:
                column, data = tag_query()
                return False, fac.AntdMessage(content=res[1], type='success'), column, data
            else:
                return False, fac.AntdMessage(content=res[1], type='error'), dash.no_update, dash.no_update
        
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        
    
    
    # 点击更多 详情按钮
    @callback(
        Output("tagManage-info_modal", "title", allow_duplicate=True),
        Output("tagManage-info_modal", "visible", allow_duplicate=True),
        Output("tagManage-info_modal", "children", allow_duplicate=True),
        Input('tagManage-tag_table', 'nClicksDropdownItem'),
        State('tagManage-tag_table', 'recentlyClickedDropdownItemTitle'),
        State('tagManage-tag_table', 'recentlyDropdownItemClickedRow'),
        prevent_initial_call=True,
    )
    def tagManage_table_dropdown_update(nClicksDropdownItem,
                                  recentlyClickedDropdownItemTitle,
                                  recentlyDropdownItemClickedRow):
        
        if recentlyClickedDropdownItemTitle == '详情':
            res = tag_info(recentlyDropdownItemClickedRow)
            return f"详情@{recentlyDropdownItemClickedRow['tag_key']}", True, res
        else:
            return dash.no_update, dash.no_update, dash.no_update