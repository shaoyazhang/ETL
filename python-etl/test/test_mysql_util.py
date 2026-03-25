from unittest import TestCase
from util.mysql_util import MySQLUtil, get_processed_files
from util.logging_util import init_logger
import config.project_config as config

logger = init_logger()

class TestMySQLUtil(TestCase):
    def setUp(self):
        self.mysql_uil = MySQLUtil() # 默认连接metadata数据库
        pass
    
    def test_self_autocommit(self):
        self.mysql_uil.select_db('test')
        logger.debug("使用数据库test")
        
        self.mysql_uil.execute_with_autocommit(
            'drop table if exists test_unit'
        )
        
        
        if not self.mysql_uil.check_table_existes('test', 'test_unit'):
            self.mysql_uil.create_table(
                'test', 
                'test_unit',
                'id int primary key, name varchar(255)')
            
        self.mysql_uil.execute_with_autocommit(
            'INSERT INTO test_unit VALUES (1, "潇潇"), (2, "甜甜")'
        )
        
        self.mysql_uil.close_conn()
        
        # 验证是否提交到数据库
        util = MySQLUtil()
        util.select_db('test')
        query_ret = util.query('select* from test_unit')
        self.assertEqual(query_ret, ((1, "潇潇"), (2, "甜甜")))
        util.close_conn()
        
        

    def test_autocommit_true(self):
        self.mysql_uil.select_db('test')
        logger.debug("使用数据库test")
        self.mysql_uil.execute_with_autocommit(
            'drop table if exists test_unit'
        )
        
        self.mysql_uil.conn.autocommit(True)
        if not self.mysql_uil.check_table_existes('test', 'test_unit'):
            self.mysql_uil.create_table(
                'test', 
                'test_unit',
                'id int primary key, name varchar(255)')
            
        self.mysql_uil.execute_without_autocommit(
            'INSERT INTO test_unit VALUES (1, "潇潇"), (2, "甜甜")'
        )
        
        new_util = MySQLUtil()
        new_util.select_db('test')
        query_ret = new_util.query(
            'select* from test_unit order by id'
        )
        
        self.assertEqual(query_ret, ((1, "潇潇"), (2, "甜甜")))
        
        self.mysql_uil.close_conn()
        new_util.close_conn()
        
    
    def test_autocommit_false(self):
        self.mysql_uil.conn.autocommit(True)
        self.mysql_uil.select_db('test')
        logger.debug("使用数据库test")
        
        self.mysql_uil.execute_with_autocommit(
            'drop table if exists test_unit'
        )
        
        if not self.mysql_uil.check_table_existes('test', 'test_unit'):
            self.mysql_uil.create_table(
                'test', 
                'test_unit',
                'id int primary key, name varchar(255)')
            
        self.mysql_uil.execute_without_autocommit(
            'INSERT INTO test_unit VALUES (1, "潇潇")'
        )
        
        self.mysql_uil.close_conn()
        
        # 设置autocommit为False
        new_util = MySQLUtil()
        new_util.conn.autocommit(False)
        new_util.select_db('test')
        new_util.execute_without_autocommit(
            'INSERT INTO test_unit VALUES (2, "甜甜")'
        )
        new_util.close_conn()
        
        # 测试
        new_util2 = MySQLUtil()
        new_util2.select_db('test')
        query_ret = new_util2.query(
            'SELECT* FROM test_unit ORDER BY id'
        )
        expected = ((1, "潇潇"), )
        self.assertEqual(query_ret, expected)
    
    def test_get_processed_files(self):
        ''' 
        测试获取一杯处理过的文件列表功能的单元测试
        保证独立性，自备表和数据
        '''
        # 先清空
        self.mysql_uil.select_db('test')
        self.mysql_uil.execute_with_autocommit('DROP TABLE IF EXISTS test_file_monitor')
        # 第一个测试用例，测试空表读取的结果
        results = get_processed_files(self.mysql_uil, 'test', 'test_file_monitor')
        self.assertEqual(results, [])
        
        # 第二个测试用例
        if not self.mysql_uil.check_table_existes('test', 'test_file_monitor'):
            self.mysql_uil.create_table(
                'test',
                'test_file_monitor',
                config.metadata_file_monitor_table_create_cols
            )
        # 清空表
        self.mysql_uil.execute_with_autocommit('TRUNCATE test_file_monitor')
        # 插入数据
        self.mysql_uil.execute_with_autocommit(
            'INSERT INTO test_file_monitor VALUES(1, "d:/test_outputs/data.log", 1024, "2026-03-25 19:09:00")'
        )
        
        result1 = get_processed_files(
            self.mysql_uil,
            'test',
            'test_file_monitor',
            config.metadata_file_monitor_table_create_cols
        )
        self.assertEqual(result1, ['d:/test_outputs/data.log'])
            
        # 第三个测试用例
        self.mysql_uil.execute_with_autocommit(
            'INSERT INTO test_file_monitor VALUES(2, "d:/test_outputs/data1.log", 1024, "2026-03-25 19:09:00")'
        )
        result1 = get_processed_files(
            self.mysql_uil,
            'test',
            'test_file_monitor',
            config.metadata_file_monitor_table_create_cols
        )
        result1.sort()
        expected = ['d:/test_outputs/data.log', 'd:/test_outputs/data1.log']
        expected.sort()
        self.assertEqual(result1, expected)
        self.mysql_uil.close_conn()
        pass
    def tearDown(self):
        pass