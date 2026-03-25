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
            logger.info(f'构建完成到{host}:{port}的数据库{database}的连接')
      
    def query(self, sql):
        """
        Args:
            sql (_type_): 需要执行的查询语句
            return: 查询结果
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        logger.info(f'执行完查询语句：{sql}, 执行结果：{result}')
        return result
    
    
    def select_db(self, db_name):
        """
        Args:
            db (数据库): 需要切换的数据库
            return: None
        """
        # cursor = self.conn.cursor()
        # cursor.execute('use ' + db_name + ';')
        sql_syntax = 'use ' + db_name + ';'
        logger.info(f'当前执行的sql语句 {sql_syntax}')
        self.conn.select_db(db_name)
        
    def execute_with_autocommit(self, sql):
        """
        直接执行一条SQL语句，不处理返回值
        需要确保执行的SQL语句提交到数据库
        Args:
            sql (sql语句): 需要执行的sql语句
        """
        cursor = self.conn.cursor()
        # 执行sql
        cursor.execute(sql)  
        logger.debug(f'执行了一条SQL: {sql}')
        
        # 确保提交到数据库
        if not self.conn.get_autocommit():
            self.conn.commit() #通过connection 提交
            # 关闭游标
            cursor.close()
    def execute_without_autocommit(self, sql):
        """
        直接执行一条SQL语句，不处理返回值
        不会判断自动提交，只执行不会commit
        Args:
            sql (_type_): 需要执行的sql语句
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        logger.debug(f'执行了一条SQL: {sql}')
        
    def check_table_existes(self, db_name, table_name):
        """
        检查给定的数据库下，给定的表，是否存在
        Args:
            db_name (_type_): 数据库名称
            table_name (_type_): 表名
        """
        # 切换数据库
        self.conn.select_db(db_name)
        # 查询所有的tables
        results = self.query('SHOW TABLES')
        # 判断待查询的表是否在结果中
        # 因为结果是tuple: ('test', )
        return (table_name, ) in results
        
    
    def create_table(self, db_name, table_name, create_cols):
        """
        检查给定的数据库下给定的表，是否存在
        如果不存在就创建
        Args:
            db_name (_type_): 数据库名称
            table_name (_type_): 表名
            create_cols (_type_): 字段名以及类型
        """
        
        # if not self.check_table_existes(db_name, table_name):
        create_sql = f'CREATE TABLE {table_name} ({create_cols})'
        # 切换数据库
        self.conn.select_db(db_name)
        self.execute_with_autocommit(create_sql)
        logger.info(f'数据库：{db_name} 中创建了表：{table_name}')
        # else:
            # logger.inf(f'数据库：{db_name}中，表{table_name}已经存在')
            
    
    def close_conn(self):
        if self.conn:
            self.conn.close()
            self.conn = None # 防御性编程
    
def get_processed_files(db_util, 
                        db_name=config.metadata_database, 
                        table_name=config.metadata_file_monitor_table_name, 
                        create_cols=config.metadata_file_monitor_table_create_cols):
    """_summary_
    获取处理过的文件名
    Args:
        db_util (_type_): MySQLUtil实例对象
        db_name (_type_, optional): 数据库名称. 默认metadata_database.
        table_name (_type_, optional): 元数据库名称. 默认metadata_file_monitor_table_name.
        create_cols (_type_, optional): 建表语句. 默认metadata_file_monitor_table_create_cols.
        return: 处理过的文件路径组成的列表
    """
    db_util.select_db(db_name)
    # 判断元数据表是否存在
    if not db_util.check_table_existes(db_name, table_name):
        # 如果不存在就建表
        db_util.create_table(db_name, table_name, create_cols)
        return []
    else:
        logger.debug(f'{table_name}已经存在，跳过建表')
    
    # 查询元数据表中存的处理过的文件名
    results = db_util.query(
        f'SELECT file_name FROM {table_name}')
    # results是一个元祖 (('file1', ), ('file2', ))
    file_names = []
    for result in results:
        file_names.append(result[0])
        
    return file_names
     
    
if __name__ == '__main__':
    # 链接到元数据库
    mysql_util = MySQLUtil()
    mysql_util.query('select* from test')
    mysql_util.select_db('retail')
    mysql_util.query('SELECT database()')   # 查询现在的数据库
    # mysql_util.execute_with_autocommit()
    
    if not mysql_util.check_table_existes('metadata', 'test2'):
        mysql_util.create_table('metadata', 'test2', 'age int, name varchar(255)')
    mysql_util.close_conn()
    # 链接到目的地数据库
    # target_mysql_util = MySQLUtil(
    #     host=config.target_host,
    #     port=config.target_port,
    #     password = config.metadata_password,
    #     charset = config.mysql_charset,
    #     database = config.target_database
    # )
    
    