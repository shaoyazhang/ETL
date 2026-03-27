import sys
from pathlib import Path
import json
import pymysql
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
from model.retail_orders_model import OrderModel, OrderDetailModel

logger = init_logger()
logger.setLevel(20) # 设置日志级别
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

processed_file_records_dict = {} # 记录每个文件处理了多少条数据，key是文件名，value是处理的订单数据条数

# 4. 依次处理待处理的json文件
## 4.1 读取json文件内容, 循环读取每一个文件
for filename in need_to_process_files:
    
    file_processed_line_count = 0 # 记录当前文件处理了多少条订单数据
    # 存储所有的订单模型
    order_model_list = []
    # 存储所有的订单详情模型
    order_detail_model_list = []
    
    ## 4.2 根据读取的json字符串，生成OrderMode, OrderDetailModel
    with open(Path(config.json_root_path) / filename, 'r', encoding='utf-8') as f:
        for line in f:
            file_processed_line_count += 1 # 订单数据条数加1
            order_model = OrderModel(data=line) # 一笔订单数据
            order_detail_model = OrderDetailModel(data=line) # 一笔订单中的订单详情数据
            order_model_list.append(order_model)
            order_detail_model_list.append(order_detail_model) 
            
    # 这个循环结束后，一个json文件处理完成
    ## 4.3 对数据进行过滤
    received_models = [model for model in order_model_list if model.receivable <= 10000]
    ## 4.4 把得到的模型中的数据写入到csv文件
    # 把订单信息写入到csv文件，order_csv_write_f -> 文件句柄
    order_csv_write_f = open(
        file = config.retail_output_csv_root_path + "/" + config.retail_orders_output_csv_filename,
        mode = 'a',
        encoding = 'utf-8'
    )
    for model in received_models:
        line = model.to_csv()
        order_csv_write_f.write(line + '\n')
        
    order_csv_write_f.close()
    
    # 把订单详情信息写入到csv文件，order_detail_dsv_write_f -> 文件句柄
    order_detail_dsv_write_f = open(
        file = config.retail_output_csv_root_path + "/" + config.retail_order_detail_output_csv_filename,
        mode = 'w',
        encoding = 'utf-8'
    )

    for model in order_detail_model_list:
        line = model.to_csv()
        # order_detail_dsv_write_f.write(line + '\n')
        order_detail_dsv_write_f.write(line) # 我这里没有加换行符 '\n', 是因为json文件已经包含换行了
    order_detail_dsv_write_f.close()
    # 记录当前文件处理了多少条订单数据
    processed_file_records_dict[filename] = file_processed_line_count
    
    logger.debug(f'json文件{filename}处理完成了！写出到了{config.retail_output_csv_root_path}目录下！')
    ## 4.5 把得到的模型中的数据写入到SQL数据库
    ### 构造MySQLUtil对象，连接到目的地数据库
    target_util = MySQLUtil(
        host=config.target_host,
        port =config.target_port,
        user=config.target_user,
        password=config.target_password,
        database=config.target_database,
        charset=config.mysql_charset
    )

    # 判断order, order_detail表是否存在，如果不存在则创建表
    if not target_util.check_table_existes(
        config.target_database,
        config.target_orders_table_name,
    ):
        target_util.create_table(
            config.target_database,
            config.target_orders_table_name,
            config.target_orders_table_create_cols
        )
        
    for i, model in enumerate(received_models):
        sql = model.generate_insert_sql()
        # 切换数据库
        target_util.select_db(config.target_database)
        target_util.execute_without_autocommit(sql)
        if (i + 1) % 1000 == 0: # 每1000条数据提交一次事务
            target_util.conn.commit()
            
    target_util.conn.commit() # 提交剩余的不足1000条的数据     
    logger.debug(f'{filename}订单数据已经写入到目的地数据库的{config.target_orders_table_name}表中了！')
    # order_detail表的写入
    if not target_util.check_table_existes(
        config.target_database,
        config.target_order_detail_table_name,
    ):
        target_util.create_table(
            config.target_database,
            config.target_order_detail_table_name,
            config.target_orders_detail_table_create_cols
        )
        
    for i, model in enumerate(order_detail_model_list):
        sql = model.generate_insert_sql()
        # 切换数据库
        target_util.select_db(config.target_database)
        target_util.execute_without_autocommit(sql)
        if (i + 1) % 1000 == 0: # 每1000条数据提交一次事务
            target_util.conn.commit()
    
    target_util.conn.commit() # 提交剩余的不足1000条的数据
    logger.debug(f'订单详情数据已经写入到目的地数据库的{config.target_order_detail_table_name}表中了！')
    target_util.close_conn() # 关闭目的地数据库的连接
global_count = sum(processed_file_records_dict.values())

logger.debug(f"完成了CSV备份文件的写出，写出到了{config.retail_output_csv_root_path}目录下！")
logger.debug(f"完成了SQL数据库的写入，写入到了目的地数据库的{config.target_orders_table_name}表和{config.target_order_detail_table_name}表中！")
logger.debug(f"总共处理了{global_count}条订单数据！")

metadata_db_util = MySQLUtil()

for filename, processed_lines in processed_file_records_dict.items():
    file_name = Path(filename).as_posix() if filename else ''
    file_name_safe = file_name.replace("'", "''")
    insert_sql = f"INSERT IGNORE INTO {config.metadata_file_monitor_table_name} (file_name, proces_line) VALUES ('{file_name_safe}', {processed_lines})"
    metadata_db_util.execute_with_autocommit(insert_sql)

metadata_db_util.close_conn()
logger.debug(f"已经把处理过的文件名和处理的订单数据条数记录到了元数据库的{config.metadata_file_monitor_table_name}表中！")