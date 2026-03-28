""" 
日志模型定义
"""
from util.str_util import check_str_null_and_transform_to_sql_null, check_number_null_and_transform_to_sql_null, check_str_null_and_transform_to_sql_null, check_null
from util.time_util import ts13_to_date_str

class LogModel:
    def __init__(self, timestamp, log_level, module, response_time, province, city, message):
        self.timestamp = timestamp
        self.log_level = log_level
        self.module = module
        self.response_time = response_time
        self.province = province
        self.city = city
        self.message = message

    def __str__(self):
        return f"{self.timestamp}\t{self.log_level}\t{self.module}\t{self.response_time}\t{self.province}\t{self.city}\t{self.message}"
    
    def _safe_str(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        return str(value)
    
    def check_and_transform_area(self):
        """检查并转换省市信息，确保它们不为None，并且是字符串类型"""
        
        if check_null(self.province):
            self.province = "未知省份"
        if check_null(self.city):
            self.city = "未知城市"
        
    def to_csv(self, sep=','):
        return sep.join([
            self._safe_str(self.timestamp),
            self._safe_str(self.log_level), 
            self._safe_str(self.module),
            self._safe_str(self.response_time),
            self._safe_str(self.province),
            self._safe_str(self.city),
            self._safe_str(self.message)
        ])
    
    
    def generate_insert_sql(self, table_name):
        sql = f"""
        INSERT INTO {table_name} (
            timestamp, log_level, module, response_time, province, city, message
        ) VALUES (
            {check_str_null_and_transform_to_sql_null(str(self.timestamp))}, 
            {check_str_null_and_transform_to_sql_null(str(self.log_level))}, 
            {check_str_null_and_transform_to_sql_null(str(self.module))}, 
            {check_number_null_and_transform_to_sql_null(self.response_time)}, 
            {check_str_null_and_transform_to_sql_null(str(self.province))}, 
            {check_str_null_and_transform_to_sql_null(str(self.city))}, 
            {check_str_null_and_transform_to_sql_null(str(self.message))}
        );
        """
        return sql
    
