from unittest import TestCase
from util.file_util import get_dir_files_list, get_new_by_compare_lists
import os
from pathlib import Path
class TestFileUtil(TestCase):
    '''
    手动创建项目根目录下目录及文件，便于测试，解耦合
    Pthlib:
        parent：上一级
        parents[0]：上一级
        parents[1]：上两级
        parents[2]：上三级
    '''
    
    def setUp(self) -> None:
        # 确定手动创建的测试目录的绝对路径
        # 获取项目的根目录
        # self.project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_root_path = Path(__file__).resolve().parents[1]

    def test_get_dir_files_list(self):
        ''' 
        测试没有开启递归调用的代码
        '''
        result1 = get_dir_files_list(self.project_root_path / 'test_dir',
                           recursive=False)
        expected = ['1', '2']
        result = []
        for p in expected:
            result.append(str(self.project_root_path / 'test_dir' / p))
        self.assertEqual(result1.sort(), result.sort())

    
    def test_get_dir_files_list_recursive(self):
        ''' 
        测试开启递归调用的代码
        '''
        result2 = get_dir_files_list(self.project_root_path / 'test_dir', recursive=True)
        expected = ['1', '2', 'inner1/3', 'inner1/4', 'inner1/inner2/5']
        result = []
        for p in expected:
            result.append(str(self.project_root_path / 'test_dir' / p))
        self.assertEqual(result.sort(), result2.sort())
    
    def test_get_new_by_compare_lists(self):
        a_list = ['e:/a.txt', 'e:/b.txt', 'e:/c.txt', 'e:/d.txt']
        b_list = ['e:/a.txt', 'e:/b.txt']
        result = get_new_by_compare_lists(a_list, b_list)
        expected = ['e:/c.txt', 'e:/d.txt']
        self.assertEqual(expected.sort(), result.sort())
        pass
    def tearDown(self) -> None:
        pass