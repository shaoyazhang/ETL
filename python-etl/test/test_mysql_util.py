from unittest import TestCase
from util.mysql_util import MySQLUtil
from util.logging_util import init_logger

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
    
    def tearDown(self):
        pass