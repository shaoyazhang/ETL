import sys
from pathlib import Path

# “动态改 Python 模块搜索路径”
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
"""
json文件处理的主要逻辑
"""
from util.logging_util import init_logger
from util.file_util import get_dir_files_list, get_new_by_compare_lists
import config.project_config as config
from util.mysql_util import MySQLUtil, get_processed_files
logger = init_logger()

# 1. 从指定的json所在的目录读取所有的json文件名
files = get_dir_files_list(path=config.json_root_path, recursive=False)
logger.debug(f'判断json的文件夹，发现有如下文件：{files}')

# 2. 从元数据库中读取已经处理过的json文件名
## 2.1 实例化MySQLUtil对象
db_util = MySQLUtil()
## 2.2 获取处理过的文件名
processed_files = get_processed_files(db_util)
logger.debug(f"查询MySQL, 找到有如下文件已经被处理过了：{processed_files}")

# 3. 通过比较函数获取待处理的json文件名
need_to_process_files = get_new_by_compare_lists(files, processed_files)
logger.debug(f'经过对比mysql元数据库，找出如下文件供我们处理：{need_to_process_files}')