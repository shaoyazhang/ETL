''' 
这是一个MySQL的工具类
提供操作MySQL的相关功能
提供的功能有：
    - 创建MySQL的链接
    - 关闭链接
    - 执行SQL查询的功能，并返回查询结果
    - 执行一条单独的无返回值的SQL语句(CREATE, UPDATE)
    - 创建表
    - 查看表是否存在
'''

import pymysql

class MySQLUtil:
    def __init__(self):
        ''' 
        创建MySQL的链接
        '''
        host = 'localhost',
        port = 3306, # 一定是整型
        user = 'root',
        password = 'Alph@2025',
        charset = 'utf8' # utf8不是utf-8
      
    def query(self, sql):
        pass
    def select_db(self, db):
        """_summary_

        Args:
            db (数据库): 需要切换的数据库
            return: None
        """
        
    def execute_with_autocommit(self, sql):
        """_summary_

        Args:
            sql (sql语句): 需要执行的sql语句
        """
    
    
    def execute_without_autocommit(self, sql):
        """_summary_

        Args:
            sql (_type_): 需要执行的sql语句
        """
    def check_table_existes(self, db_name, table_name):
        """_summary_

        Args:
            db_name (_type_): 数据库名称
            table_name (_type_): 表名
        """
        pass
    
    def check_table_exists_and_create(self, db_name, table_name, create_cols):
        """_summary_

        Args:
            db_name (_type_): 数据库名称
            table_name (_type_): 表名
            create_cols (_type_): 字段名以及类型
        """
        pass
    
    def close(self):
        pass