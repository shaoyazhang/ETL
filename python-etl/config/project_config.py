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
target_host = metadata_host
target_port = metadata_port # 一定是整型
target_user = metadata_user
target_password = metadata_password
target_database = 'retail' # 当前处理的是元数据，所以可以先写metadata
##################### 目的地库配置 end ###########################

##################### json 相关配置 start ###########################
json_root_path = 'D:\\Pythons_studies\\logs\\json'
##################### json 相关配置 end ###########################

# 目的地表配置
target_orders_table_name = 'orders'
# orders表的建表语句的列信息
target_orders_table_create_cols = """
    order_id VARCHAR(255) PRIMARY KEY,
    store_id INT COMMENT '店铺ID',
    store_name VARCHAR(30) COMMENT '店铺名称',
    store_status VARCHAR(10) COMMENT '店铺状态(open,close)',
    store_own_user_id INT COMMENT '店主id',
    store_own_user_name VARCHAR(50) COMMENT '店主名称',
    store_own_user_tel VARCHAR(15) COMMENT '店主手机号',
    store_category VARCHAR(10) COMMENT '店铺类型(normal,test)',
    store_address VARCHAR(255) COMMENT '店铺地址',
    store_shop_no VARCHAR(255) COMMENT '店铺第三方支付id号',
    store_province VARCHAR(10) COMMENT '店铺所在省',
    store_city VARCHAR(10) COMMENT '店铺所在市',
    store_district VARCHAR(10) COMMENT '店铺所在行政区',
    store_gps_name VARCHAR(255) COMMENT '店铺gps名称',
    store_gps_address VARCHAR(255) COMMENT '店铺gps地址',
    store_gps_longitude VARCHAR(255) COMMENT '店铺gps经度',
    store_gps_latitude VARCHAR(255) COMMENT '店铺gps纬度',
    is_signed TINYINT COMMENT '是否第三方支付签约(0,1)',
    operator VARCHAR(10) COMMENT '操作员',
    operator_name VARCHAR(50) COMMENT '操作员名称',
    face_id VARCHAR(255) COMMENT '顾客面部识别ID',
    member_id VARCHAR(255) COMMENT '顾客会员ID',
    store_create_date_ts TIMESTAMP COMMENT '店铺创建时间',
    origin VARCHAR(255) COMMENT '来源信息(无用)',
    day_order_seq INT COMMENT '本订单是当日第几单',
    discount_rate DECIMAL(10,5) COMMENT '折扣率',
    discount_type TINYINT COMMENT '折扣类型',
    discount DECIMAL(10,5) COMMENT '折扣金额',
    money_before_whole_discount DECIMAL(10,5) COMMENT '折扣前总金额',
    receivable DECIMAL(10,5) COMMENT '应收金额',
    erase DECIMAL(10,5) COMMENT '抹零金额',
    small_change DECIMAL(10,5) COMMENT '找零金额',
    total_no_discount DECIMAL(10,5) COMMENT '总价格(无折扣)',
    pay_total DECIMAL(10,5) COMMENT '付款金额',
    pay_type VARCHAR(10) COMMENT '付款类型',
    payment_channel TINYINT COMMENT '付款通道',
    payment_scenarios VARCHAR(15) COMMENT '付款描述(无用)',
    product_count INT COMMENT '本单卖出多少商品',
    date_ts TIMESTAMP COMMENT '订单时间',
    INDEX (receivable),
    INDEX (date_ts)
"""


# JSON数据采集后，写入MYSQL, 存储订单详情（待商品信息的）相关的表，表名是：
target_order_detail_table_name = 'order_detail'
# order_detail表的建表语句的列信息
target_orders_detail_table_create_cols = """
    order_id VARCHAR(255) COMMENT '订单ID',
    barcode VARCHAR(255) COMMENT '商品条码',
    name VARCHAR(255) COMMENT '商品名称',
    count INT COMMENT '本单此商品卖出数量',
    price_per DECIMAL(10,5) COMMENT '实际售卖单价',
    retail_price DECIMAL(10,5) COMMENT '零售建议价',
    trade_price DECIMAL(10,5) COMMENT '贸易价格(进货价)',
    category_id INT COMMENT '商品类别ID',
    unit_id INT COMMENT '商品单位ID(包、袋、箱、等)',
    PRIMARY KEY (order_id, barcode)
"""

# CSV文件输出的根目录
retail_output_csv_root_path = 'D:\\Pythons_studies\\logs\\csv'
# CSV文件输出的订单信息文件名，包含时间戳
retail_orders_output_csv_filename = f'orders-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'
# CSV文件输出的订单详情信息文件名，包含时间戳
retail_order_detail_output_csv_filename = f'order_detail-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'