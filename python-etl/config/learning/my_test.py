# def add(a:float, b:float) -> float:
#     return a + b

import json


# class Person:
#     def __init__(self, name: str, age: int, address: str):
#         self.name = name
#         self.age = age
#         self.address = address

#     def to_csv(self, sep: str = ',') -> str:
#         return f'{self.name}{sep}{self.age}{sep}{self.address}'
    
#     def to_sql(self):
#         return f"INSERT INTO person VALUES ('{self.name}', {self.age}, '{self.address}');"
    
# jstr = """{"name": "Alice", "age": 30, "address": "123 Main St"}"""   
# d = json.loads(jstr)
# p1 = Person(d['name'], d['age'], d['address'])
# print(p1.to_csv())  # 输出: Alice,30,123 Main St   
# print(p1.to_sql())  # 输出: INSERT INTO person VALUES ('Alice', 30, '123 Main St'); 


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

from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).parents[2]
print(CURRENT_DIR)
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
from util.mysql_util import MySQLUtil
    
db_util = MySQLUtil(database='test')
db_util.create_table('test', 'test_order_details', target_orders_detail_table_create_cols)
