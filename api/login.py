import sqlite3
import dash
from common.sql import SQLiteClass


def login(username, password):

    with SQLiteClass("./acebergBehavior.db") as cursor:
        user = cursor.select_data("users",columns="role" ,condition="account='{}' and password='{}'".format(username, password))

    if user:
        # 调更新登陆状态的方法
        updateres = update_loginstatus(username, password, 1)
        if updateres[0]:
            return True, 200, 'success', "登录成功"
        else:
            return False, 200, 'error', "登录状态更新失败"
    else:
        return False, 200, 'error', "账户或密码错误"

def logout(username, password):

    updateres = update_loginstatus(username, password, 0)
    if updateres[0]:
        return True, 200, 'success', "退出成功"
    else:
        return False, 200, 'error', "登录状态更新失败"


def update_loginstatus(username, password, status):
    # 检查用户信息
    with SQLiteClass("./acebergBehavior.db") as cursor:
        data = cursor.update_data("users", {'loginstatus':status} ,condition="account='{}' and password='{}'".format(username, password))

    if data:
        return True, 200, 'success', "更新登陆状态成功"
    else:
        return False, 200, 'error', "更新登陆状态失败"
