""" 
日志文件处理逻辑
"""
from model.log_model import LogModel
from datetime import datetime
from util.logging_util import init_logger
from model.log_model import LogModel
from util.mysql_util import MySQLUtil
import config.project_config as config
from util.file_util import get_dir_files_list, get_new_by_compare_lists
from pathlib import Path

logger = init_logger()
logger.setLevel(20) # 设置日志级别
logger.info("开始执行日志文件处理的相关逻辑！")

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

# 2. 获取日志文件的路径列表
files = [Path(f).as_posix() for f in get_dir_files_list(config.logs_root_path)]
logger.info(f"在目录{config.logs_root_path}下找到了{len(files)}个日志文件！")

# 2.1 确保logs_monitor表存在（存储已处理的文件）
if not metadata_util.check_table_existes(config.metadata_database, config.metadata_logs_update_monitor_table_name):
    logger.info(f"元数据数据库{config.metadata_database}中不存在表{config.metadata_logs_update_monitor_table_name}，将会自动创建这个表！")
    metadata_util.create_table(
        config.metadata_database,
        config.metadata_logs_update_monitor_table_name,
        config.metadata_logs_table_create_cols
    )

# 2.2 加载已处理过的文件（logs_monitor表）
metadata_util.select_db(config.metadata_database)
processed_rows = metadata_util.query(
    f"SELECT file_name FROM {config.metadata_logs_update_monitor_table_name};"
)
processed_files = [row[0] for row in processed_rows if row and row[0]]
logger.info(f"从logs_monitor中读取到已经处理过的日志文件有{len(processed_files)}个！")

need_to_process_files = get_new_by_compare_lists(files, processed_files)
logger.info(f"经过对比，找到了{len(need_to_process_files)}个日志文件需要我们处理！")

processed_files_dict = {} # 记录每个文件处理了多少条数据，key是文件名，value是处理的日志数据条数

# 3. 依次处理每个日志文件
for file in need_to_process_files:
    logger.info(f"开始处理日志文件{file}！")
    processed_line_count = 0 # 记录当前文件处理了多少条日志数据
    log_model_list = [] # 存储当前文件中所有的日志模型
    
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 跳过表头
            if line.startswith('日志时间'):
                continue

            parts = line.split('\t')
            if len(parts) != 7:
                logger.warning(f"日志行格式不正确，跳过：{line}")
                continue

            timestamp, log_level, module, response_time_raw, province, city, message = parts
            # response_time 格式可能是 '123ms'
            response_time = response_time_raw.rstrip('ms') if response_time_raw.endswith('ms') else response_time_raw
            try:
                response_time = int(response_time)
            except Exception:
                logger.warning(f"响应时间解析失败，使用0：{response_time_raw}")
                response_time = 0

            log_model = LogModel(timestamp, log_level, module, response_time, province, city, message)
            processed_line_count += 1
            log_model_list.append(log_model)
    
    processed_files_dict[file] = processed_line_count
    logger.info(f"文件{file}处理完毕，共处理了{processed_line_count}条日志数据！")
    log_model_write_csv = open(
        file = config.logs_output_csv_root_path + "/" + config.logs_output_csv_filename,
        mode = 'a',
        encoding = 'utf-8-sig'  # 使用 utf-8-sig 添加 BOM，支持中文
    )
    for model in log_model_list:
        log_model_write_csv.write(model.to_csv() + "\n")
    log_model_write_csv.close()

    # 3.2 从日志文件中读取数据，按照时间顺序处理，写入到目的地数据库的表中
    ## 3.2.1 先检查存储日志文件处理状态的监控表是否存在，如果不存在则创建这个表
    if not target_util.check_table_existes(config.target_database, config.target_logs_table_name):
        logger.info(f"目的地数据库{config.target_database}中不存在表{config.target_logs_table_name}，将会自动创建这个表！")
        target_util.create_table(
            config.target_database,
            config.target_logs_table_name,
            config.target_logs_table_create_cols
        )
    
    for i, model in enumerate(log_model_list):
        sql = model.generate_insert_sql(config.target_logs_table_name)
        target_util.select_db(config.target_database)
        target_util.execute_without_autocommit(sql)    
        if (i + 1) % 1000 == 0: # 每1000条数据提交一次事务
            target_util.conn.commit()
            
    target_util.conn.commit() # 提交剩余的不足1000条的数据
    logger.info(f'{file}日志数据已经写入到目的地数据库的{config.target_logs_table_name}表中了！')

# 4. 把处理过的文件记录到监控表中
metadata_util.select_db(config.metadata_database)

for filename, processed_lines in processed_files_dict.items():
    file_name = Path(filename).as_posix()
    file_name_safe = file_name.replace("'", "''")
    insert_sql = f"INSERT IGNORE INTO {config.metadata_logs_update_monitor_table_name} (file_name, proces_line) VALUES ('{file_name_safe}', {processed_lines})"
    metadata_util.execute_with_autocommit(insert_sql)

metadata_util.close_conn()
target_util.close_conn()
logger.info(f"完成了日志文件的处理，处理结果已经记录到监控表{config.metadata_logs_update_monitor_table_name}中了！")