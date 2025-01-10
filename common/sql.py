import sqlite3


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

    def custom_sql(self, sql_str):
        self.cursor.execute(sql_str)
        self.conn.commit()
        data = self.cursor.fetchall()
        # return self.cursor.fetchone()  # return only one row
        # 获取列名
        column_names = [description[0] for description in self.cursor.description]
        # 转成 JSON 格式
        json_data = [dict(zip(column_names, row)) for row in data]
        return json_data 





    # 执行返回受影响的行数
    # def execute(self, sql, params=None):
    #     self.cursor.execute(sql, params)
    #     self.conn.commit()
    #     return self.cursor.rowcount
    # def execute(self, query, values=None):
    #     cursor = self.conn.cursor()
    #     try:
    #         if values:
    #             cursor.execute(query, values)
    #         else:
    #             cursor.execute(query)
    #         return cursor.rowcount > 0  # 返回是否至少有一行被更新
    #     except sqlite3.Error as e:
    #         print(f"An error occurred: {e}")
    #         return False  # 明确返回 False 表示更新失败
