from unittest import TestCase, main
from my_test import add
class MyTest(TestCase):
    def setUp(self) -> None: # 测试时需要提前执行的代码
        pass
    
    def test_myfunc(self):
        a = add(1, 2)
        self.assertEqual(a, 3)
    
    def tearDown(self) -> None: # 收尾的工作。比如：关闭连接
        pass
    
