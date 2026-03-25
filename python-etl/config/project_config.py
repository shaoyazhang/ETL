import time
log_root_path = "D:/Pythons_studies/logs/"
log_filename = f'pyetl-{time.strftime("%Y%m%d-%H", time.localtime(time.time()))}.log'

level = 10



##################### MySQLUtil配置 ##########################
mysql_charset = 'utf8' # utf8不是utf-8
##################### 原数据库配置 start ###########################
metadata_host = 'localhost'
metadata_port = 3306 # 一定是整型
metadata_user = 'root'
metadata_password = 'Alph@2025'
metadata_database = 'metadata' # 当前处理的是元数据，所以可以先写metadata

# 文件监控表名称，存储哪些文件被处理过
metadata_file_monitor_table_name = 'file_monitor'
# 文件监控表，建表语句的列信息
metadata_file_monitor_table_create_cols = """
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255) UNIQUE NOT NULL COMMENT '被处理的文件名称',
    proces_line INT COMMENT '本文件中有多少条数据被处理',
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '处理时间'

"""


##################### 原数据库配置 end ###########################


##################### 目的地库配置 start ###########################
target_host = 'localhost'
target_port = 3306 # 一定是整型
target_user = 'root'
target_password = 'Alph@2025'
target_database = 'retail' # 当前处理的是元数据，所以可以先写metadata
##################### 目的地库配置 end ###########################

##################### json 相关配置 start ###########################
json_root_path = 'D:\\Pythons_studies\\logs/json'
