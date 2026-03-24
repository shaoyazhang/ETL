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
##################### 原数据库配置 end ###########################
