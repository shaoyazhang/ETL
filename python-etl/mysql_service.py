from util.logging_util import init_logger
from util.mysql_util import MySQLUtil
import config.project_config as config
import sys
from datetime import datetime
from model.barcode_model import BarcodeModel
from pathlib import Path
""" 
mysql数据库服务的主要逻辑
"""
logger = init_logger()
logger.setLevel(20) # 设置日志级别
logger.info("开始执行MySQL数据库服务的相关逻辑！")

# 1. 构建数据库util对象
metadata_util = MySQLUtil()
target_util = MySQLUtil(
    host=config.target_host,
    port=config.target_port,
    user=config.target_user,
    password=config.target_password,
    database=config.target_database,
    charset=config.mysql_charset
)

source_util = MySQLUtil(
    host=config.source_host,
    port=config.source_port,
    user=config.source_user,
    password=config.source_password,
    database=config.source_database,
    charset=config.mysql_charset
)


# 2. 从数据源中读取数据
## 2.1 判断数据源是否存在
if not source_util.check_table_existes(config.source_database, config.source_barcode_data_table_name):
    logger.error(f"数据源数据库{config.source_database}中不存在表{config.source_barcode_data_table_name}，请检查数据源数据库的配置和数据准备情况！")
    sys.exit(1)
    
# 3. 目的地的MySQL数据库中，是否有我们要写入数据的表? 如果没有，那么新建
if not target_util.check_table_existes(config.target_database, config.target_barcode_table_name):
    logger.info(f"目的地数据库{config.target_database}中不存在表{config.target_barcode_table_name}，将会自动创建这个表！")
    target_util.create_table(
        config.target_database,
        config.target_barcode_table_name,
        config.target_barcode_table_create_cols
    )

# 4. 写入数据，目的地数据库(retail), csv文件
metadata_util.select_db(config.metadata_database)
last_update_time = None
# 从原数据表中读取上一批次更新的最后更新时间
if not metadata_util.check_table_existes(config.metadata_database, 
                                         config.metadata_barcode_update_monitor_table_name):
    logger.info(f"元数据数据库{config.metadata_database}中不存在表{config.metadata_barcode_update_monitor_table_name}，将会自动创建这个表！")
    metadata_util.create_table(
        config.metadata_database,
        config.metadata_barcode_update_monitor_table_name,
        config.metadata_barcode_table_create_cols
    )
    
else:
    # 降序排序，去除第一个
    query_sql = f"SELECT time_record FROM {config.metadata_barcode_update_monitor_table_name} ORDER BY time_record DESC LIMIT 1;"
    result = metadata_util.query(query_sql)
    # ((,),) 这种格式，需要取出里面的值
    if result and len(result) > 0:
        last_update_time = str(result[0][0])
        logger.info(f"上次采集的最后更新时间是{last_update_time}，本次将从这个时间点之后的数据开始采集！")
        
if last_update_time:
    sql = f"SELECT * FROM {config.source_barcode_data_table_name} WHERE update_at >= '{last_update_time}' ORDER BY update_at ASC;"
else:
    sql = f"SELECT * FROM {config.source_barcode_data_table_name} ORDER BY update_at ASC;"
    
source_util.select_db(config.source_database)
result = source_util.query(sql)
# print(result[:2])
print(f"查询到的数据行数: {len(result)}")

# 构造存储对象列表
barcode_model_list = []
for single_line_result in result:
    model = BarcodeModel(
        code=single_line_result[0],
        name=single_line_result[1],
        spec=single_line_result[2],
        trademark=single_line_result[3],
        addr=single_line_result[4],
        units=single_line_result[5],
        factory_name=single_line_result[6],
        trade_price=single_line_result[7],
        retail_price=single_line_result[8],
        update_at=single_line_result[9],
        wholeunit=single_line_result[10],
        wholenum=single_line_result[11],
        img=single_line_result[12],
        src=single_line_result[13]
    )
    barcode_model_list.append(model)
    
# 写入数据，目的地数据库(retail), csv文件
# 写入到数据库 retail
max_last_update_time = datetime(2000, 1, 1)
target_util.select_db(config.target_database)
for i, model in enumerate(barcode_model_list):
    if model.update_at > max_last_update_time:
        max_last_update_time = model.update_at
    
    sql = model.generate_insert_sql()
    target_util.execute_without_autocommit(sql)
    if (i + 1) % 1000 == 0: # 每1000条数据提交一次事务
        target_util.conn.commit()
        
target_util.conn.commit() # 提交剩余的不足1000条的数据
logger.info(f'数据已经写入到目的地数据库的{config.target_barcode_table_name}表中了！')
# 写入到csv文件
barcode_csv_write_f = open(Path(config.barcode_output_csv_root_path) / config.barcode_output_csv_filename, 
                           'a', 
                           encoding='utf-8'
                           )
for i, model in enumerate(barcode_model_list):
    line = model.to_csv_line()
    barcode_csv_write_f.write(line + '\n')
    if (i + 1) % 1000 == 0:
        barcode_csv_write_f.flush() # 刷新缓冲区，写入到文件
        logger.info(f'已经写入了{i + 1}条数据到CSV文件中了！')
barcode_csv_write_f.close()
logger.info(f'数据已经写入到CSV文件中了，文件路径是{Path(config.barcode_output_csv_root_path) / config.barcode_output_csv_filename}！')
# 5. 记录MySQL元数据
metadata_util.select_db(config.metadata_database)
sql = f"""
INSERT INTO {config.metadata_barcode_update_monitor_table_name} (time_record, gather_line_count) VALUES ('{max_last_update_time}', {len(barcode_model_list)});
"""
metadata_util.execute_with_autocommit(sql)
metadata_util.close_conn() # 关闭元数据库的连接
target_util.close_conn() # 关闭目的地数据库的连接
logger.info(f"已经把本次采集的最后更新时间{max_last_update_time}") 
