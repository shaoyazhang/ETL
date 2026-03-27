from unittest import TestCase
from util.str_util import check_null, check_str_null_and_transform_to_sql_null


class TestStrUtil(TestCase):
    def setUp(self):
        pass
    
    def test_check_null(self):
        self.assertTrue(check_null(None))
        self.assertTrue(check_null(""))
        self.assertTrue(check_null("None"))
        self.assertTrue(check_null("null"))
        self.assertTrue(check_null("undefined"))
        
        self.assertFalse(check_null("0"))
        self.assertFalse(check_null("False"))
        
    def test_check_str_null_and_transform_to_sql_null(self):
        self.assertEqual(check_str_null_and_transform_to_sql_null(None), "NULL")
        self.assertEqual(check_str_null_and_transform_to_sql_null(""), "NULL")
        self.assertEqual(check_str_null_and_transform_to_sql_null("None"), "NULL")
        self.assertEqual(check_str_null_and_transform_to_sql_null("null"), "NULL")
        self.assertEqual(check_str_null_and_transform_to_sql_null("undefined"), "NULL")
        
        self.assertEqual(check_str_null_and_transform_to_sql_null("0"), "'0'")
        self.assertEqual(check_str_null_and_transform_to_sql_null(0), "'0'")
        self.assertEqual(check_str_null_and_transform_to_sql_null("False"), "'False'")