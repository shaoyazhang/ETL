""" 
用来承载业务数据的模型
"""
import sys
from pathlib import Path

# “动态改 Python 模块搜索路径”
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
from util.str_util import check_number_null_and_transform_to_sql_null, clean_str, check_str_null_and_transform_to_sql_null
import config.project_config as config


class BarcodeModel:
    def __init__(self, code=None, name=None, spec=None, trademark=None, addr=None, 
                 units=None, factory_name=None, trade_price=None, retail_price=None, 
                 update_at=None, wholeunit=None, wholenum=None, img=None, src=None):
        self.code = code
        self.name = clean_str(name)
        self.spec = clean_str(spec)
        self.trademark = clean_str(trademark)
        self.addr = clean_str(addr)
        self.units = clean_str(units)
        self.factory_name = clean_str(factory_name)
        self.trade_price = trade_price
        self.retail_price = retail_price
        self.update_at = update_at
        self.wholeunit = clean_str(wholeunit)
        self.wholenum = wholenum
        self.img = img
        self.src = src
    
    def to_csv_line(self, sep=','):
        return sep.join([
            str(self.code) if self.code else '',
            str(self.name) if self.name else '',
            str(self.spec) if self.spec else '',
            str(self.trademark) if self.trademark else '',
            str(self.addr) if self.addr else '',
            str(self.units) if self.units else '',
            str(self.factory_name) if self.factory_name else '',
            str(self.trade_price) if self.trade_price else '',
            str(self.retail_price) if self.retail_price else '',
            str(self.update_at) if self.update_at else '',
            str(self.wholeunit) if self.wholeunit else '',
            str(self.wholenum) if self.wholenum else '',
            str(self.img) if self.img else '',
            str(self.src) if self.src else ''
        ])
    
    
    def generate_insert_sql(self):
        sql = f"""
        REPLACE INTO {config.target_barcode_table_name} (
            code, name, spec, trademark, addr, units, factory_name, trade_price, retail_price, 
            update_at, wholeunit, wholenum, img, src
        ) VALUES (
            {check_str_null_and_transform_to_sql_null(str(self.code))}, 
            {check_str_null_and_transform_to_sql_null(str(self.name))}, 
            {check_str_null_and_transform_to_sql_null(str(self.spec))}, 
            {check_str_null_and_transform_to_sql_null(str(self.trademark))}, 
            {check_str_null_and_transform_to_sql_null(str(self.addr))}, 
            {check_str_null_and_transform_to_sql_null(str(self.units))}, 
            {check_str_null_and_transform_to_sql_null(str(self.factory_name))}, 
            {check_number_null_and_transform_to_sql_null(self.trade_price)}, 
            {check_number_null_and_transform_to_sql_null(self.retail_price)}, 
            {check_str_null_and_transform_to_sql_null(str(self.update_at))}, 
            {check_str_null_and_transform_to_sql_null(str(self.wholeunit))}, 
            {check_number_null_and_transform_to_sql_null(self.wholenum)}, 
            {check_str_null_and_transform_to_sql_null(str(self.img))}, 
            {check_str_null_and_transform_to_sql_null(str(self.src))}
        );
        """
        return sql