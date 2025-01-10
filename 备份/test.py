import sqlite3
from uuid import uuid4
from datetime import datetime
import random



class SQLiteClass:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self  # 返回整个 SQLiteClass 实例

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def create_table(self, *args):
        table_name = args[0]
        columns = args[1]
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.conn.commit()

    def del_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()
        
    def lastkey(self, table_name):
        self.cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        return self.cursor.fetchone()[0]
    
    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        return self.cursor.rowcount  # 返回受影响的行数

    def select_data(self, table_name, columns='*', condition=None):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # return self.cursor.fetchone()  # return only one row
        # 获取列名
        column_names = [description[0] for description in self.cursor.description]
        # 转成 JSON 格式
        json_data = [dict(zip(column_names, row)) for row in data]
        return json_data
    
    def select_columns(self, table_name, columns="*"):
        self.cursor.execute(f"SELECT {columns} FROM {table_name}")
        return [description[0] for description in self.cursor.description]
    
    def close_connection(self):
        self.conn.close()  # close the connection
        print(f"Connection to {self.db_name} closed")
    
    def update_data(self, table_name, data, condition):  # data is a dict
        self.cursor.execute(f"UPDATE {table_name} SET {','.join([f'{key} = ?' for key in data.keys()])} WHERE {condition}", list(data.values()))
        self.conn.commit()
        return self.cursor.rowcount
    
    def update_column(self, table_name, column_name, value, condition):
        self.cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {condition}", [value])
        self.conn.commit()
    
    def delete_data(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()
        
import hashlib

# SHA-256 哈希函数
def sha256_encrypt(password):
    # 创建 SHA-256 哈希对象
    sha256_hash = hashlib.sha256()
    # 更新哈希对象
    sha256_hash.update(password.encode())
    # 返回十六进制表示的哈希值
    return sha256_hash.hexdigest()



createtimes = [
    '2022-08-08 21:08:08',
    '2022-09-11 18:08:08',
    '2022-10-11 23:08:08',
    '2022-11-14 07:08:08',
    '2022-12-21 01:08:08',
    '2023-01-30 16:08:08',
    '2023-02-08 09:08:08',
    '2023-03-04 04:08:08',
 ]
last_browsers = [
    'Chrome',
    'Firefox',
    'Edge',
    'Safari',
    'Opera'
]

last_oss = [
    'Windows',
    'MacOS',
    'Linux',
    'Android',
    'iOS'
]

last_locs = [
    "中国-吉林省-通化市-二道江区",
    "中国-北京市-北京市-朝阳区",
    "中国-上海市-上海市-浦东新区",
    "中国-广东省-广州市-天河区",
    "中国-浙江省-杭州市-西湖区",
    "中国-江苏省-南京市-鼓楼区",
    "中国-四川省-成都市-武侯区",
    "中国-湖北省-武汉市-江汉区",
    "中国-天津市-天津市-和平区",
    "中国-重庆市-重庆市-渝中区",
]
    
# def adddata():
    
#     for i in range(3888):
#         rand = random.random()
#         uid = str(uuid4())
#         with SQLiteClass("acebergBehavior.db") as db:
#             db.insert_data("users", 
#                 {
#                     "key": f"user_{uid}", 
#                     "account": f"account_{i}",
#                     "password": sha256_encrypt("admin"),
#                     "role": "user",
#                     "sex": "男" if i % 4 == 0 else "女",
#                     "isdel": "0",
#                     "creator": "admin",
#                     "createtime": createtimes[int(rand*10) if int(rand*10) < 8 else 0],
#                     "phone": str( (13888880000+ i)),
#                     "email": f"account_{i}@163.com",
#                     "status": "active" if i % 7 == 0 else "logoff",
#                     "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                     "last_ip": "127.0.0.1",
#                     "last_device": "iPhone 16",
#                     "last_browser": last_browsers[int(rand*10) if int(rand*10) < 5 else 0],
#                     "last_os": last_oss[int(rand*10) if int(rand*10) < 5 else 0],
#                     "last_loc": last_locs[int(rand*10) if int(rand*10) < 10 else 0],
#                 })
    





def readtxt(file):
    count = 24
    # 打开文件
    with open(file, 'r', encoding='utf-8') as file:
        # 逐行读取
        for line in file:
            with SQLiteClass("acebergBehavior.db") as db:
                db.insert_data("eventManage", 
                    {
                        "key": f"event_{count}",
                        "eventKey": "",
                        "eventName": line.strip(),
                        "eventDesc": line.strip(),
                        "isdel": "0",
                        "creator": "admin",
                        "createtime": "2024-12-01 08:08:08",
                        "eventCategory": "",
                    })
            count = count + 1

readtxt('备份/事件.txt')