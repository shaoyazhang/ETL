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
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from util.logging_util import init_logger
import config.project_config as config
logger = init_logger()
class MySQLUtil:
    def __init__(self, 
                host = config.metadata_host, 
                port = config.metadata_port, # 一定是整型
                user = config.metadata_user,
                password = config.metadata_password,
                charset = config.mysql_charset, # utf8不是utf-8
                database = config.metadata_database, # 当前处理的是元数据，所以可以先写metadata
                autocommit = False  # 默认无自动提交
                ):
        ''' 
        创建MySQL的链接
        '''
        self.conn = pymysql.connect(
            host = host,
            port = port, 
            user = user,
            password = password,
            charset = charset, 
            database = database, 
            autocommit = autocommit 
        )
        if self.conn:
            logger.info('数据库链接建立成功')
      
    def query(self, sql):
        """_summary_

        Args:
            sql (_type_): 需要执行的查询语句
            return: 查询结果
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        logger.info(result)
        return result
    
    
    def select_db(self, db_name):
        """_summary_

        Args:
            db (数据库): 需要切换的数据库
            return: None
        """
        # cursor = self.conn.cursor()
        # cursor.execute('use' + db_name + ';')
        self.conn.select_db(db_name)
        
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
        if self.conn:
            self.conn.close()
            self.conn = None # 防御性编程
    
    
    
if __name__ == '__main__':
    mysql_util = MySQLUtil()
    # mysql_util.close()
    # query_result = mysql_util.query('select* from test')
    # logger.info(query_result)
    mysql_util.query('select* from test')
    mysql_util.select_db('retail')
    mysql_util.query('SELECT database()')   # 查询现在的数据库
    mysql_util.close()
    