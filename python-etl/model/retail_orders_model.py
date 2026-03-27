""" 
定义订单模型
"""
import sys
from pathlib import Path

CURRENTROOT_DIR = Path(__file__).parents[1]
if str(CURRENTROOT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENTROOT_DIR))
    
import json
from util.time_util import ts13_to_date_str
from util.str_util import check_null
import config.project_config as conf 
from util.str_util import check_str_null_and_transform_to_sql_null

class OrderModel:
    def __init__(self, data: str):
        """ 
        从传入的字符串数据构建订单model
        此model质保函订单信息，不包含订单详情（商品售卖）
        """
        
        # 将一行字符串json转换为字典对象
        data = json.loads(data)

        self.discount_rate = data['discountRate']             # 折扣率
        self.store_shop_no = data['storeShopNo']              # 店铺店号（无用）
        self.day_order_seq = data['dayOrderSeq']              # 本单为当日第几单
        self.store_district = data['storeDistrict']           # 店铺所在行政区
        self.is_signed = data['isSigned']                     # 是否签约店铺（0,1）
        self.store_province = data['storeProvince']           # 店铺所在省
        self.origin = data['origin']                          # 原始信息（无用）
        self.store_gps_longitude = data['storeGPSLongitude']  # 店铺GPS经度
        self.discount = data['discount']                      # 折扣金额
        self.store_id = data['storeID']                       # 店铺ID
        self.product_count = data['productCount']             # 本单售卖商品数量
        self.operator_name = data['operatorName']             # 操作员姓名
        self.operator = data['operator']                      # 操作员ID
        self.store_status = data['storeStatus']               # 店铺状态
        self.store_own_user_tel = data['storeOwnUserTel']     # 店铺店主电话
        self.pay_type = data['payType']                       # 支付类型
        self.discount_type = data['discountType']             # 折扣类型
        self.store_name = data['storeName']                   # 店铺名称
        self.store_own_user_name = data['storeOwnUserName']   # 店铺店主名称
        self.date_ts = data['dateTS']                         # 订单时间
        self.small_change = data['smallChange']               # 找零金额
        self.store_gps_name = data['storeGPSName']            # 店铺GPS名称
        self.erase = data['erase']                            # 是否抹零
        self.store_gps_address = data['storeGPSAddress']      # 店铺GPS地址
        self.order_id = data['orderID']                       # 订单ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前总金额
        self.store_category = data['storeCategory']           # 店铺类别
        self.receivable = data['receivable']                  # 收款金额
        self.face_id = data['faceID']                         # 面部识别ID
        self.store_own_user_id = data['storeOwnUserId']       # 店铺店主ID
        self.payment_channel = data['paymentChannel']         # 付款通道
        self.payment_scenarios = data['paymentScenarios']     # 付款情况（无用）
        self.store_address = data['storeAddress']             # 店铺地址
        
        self.total_no_discount = data['totalNoDiscount']      # 整体价格（无折扣）
        self.payed_total = data['payedTotal']                # 已付款金额
        self.store_gps_latitude = data['storeGPSLatitude']   # 店铺GPS纬度
        self.store_create_date_ts = data['storeCreateDateTS'] # 店铺创建时间
        self.store_city = data['storeCity']                  # 店铺所在城市
        self.member_id = data['memberID']                    # 会员ID
        
        
    def _safe_str(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        return str(value)

    def to_csv(self, sep=','):
        """ 将订单model转换为csv字符串，字段顺序与建表语句一致 """
        self.check_and_transform_area()
        return sep.join([
            self._safe_str(self.order_id),
            self._safe_str(self.store_id),
            self._safe_str(self.store_name),
            self._safe_str(self.store_status),
            self._safe_str(self.store_own_user_id),
            self._safe_str(self.store_own_user_name),
            self._safe_str(self.store_own_user_tel),
            self._safe_str(self.store_category),
            self._safe_str(self.store_address),
            self._safe_str(self.store_shop_no),
            self._safe_str(self.store_province),
            self._safe_str(self.store_city),
            self._safe_str(self.store_district),
            self._safe_str(self.store_gps_name),
            self._safe_str(self.store_gps_address),
            self._safe_str(self.store_gps_longitude),
            self._safe_str(self.store_gps_latitude),
            self._safe_str(self.is_signed),
            self._safe_str(self.operator),
            self._safe_str(self.operator_name),
            self._safe_str(self.face_id),
            self._safe_str(self.member_id),
            self._safe_str(ts13_to_date_str(self.store_create_date_ts)),
            self._safe_str(self.origin),
            self._safe_str(self.day_order_seq),
            self._safe_str(self.discount_rate),
            self._safe_str(self.discount_type),
            self._safe_str(self.discount),
            self._safe_str(self.money_before_whole_discount),
            self._safe_str(self.receivable),
            self._safe_str(self.erase),
            self._safe_str(self.small_change),
            self._safe_str(self.total_no_discount),
            self._safe_str(self.payed_total),
            self._safe_str(self.pay_type),
            self._safe_str(self.payment_channel),
            self._safe_str(self.payment_scenarios),
            self._safe_str(self.product_count),
            self._safe_str(ts13_to_date_str(self.date_ts))
        ])
        
    def check_and_transform_area(self):
        """ 
        检查并转换店铺所在行政区
        检查模型中的省市区三个字段，如果无意义，就转换成未知
        """
        if check_null(self.store_province):
            self.store_province = "未知省份"
            
        if check_null(self.store_city):
            self.store_city = "未知城市"
            
        if check_null(self.store_district):
            self.store_district = "未知区县"
            
            
    def generate_insert_sql(self):
        """ 生成插入订单数据的sql语句 """
        self.check_and_transform_area()
        sql = f"""
        INSERT IGNORE INTO {conf.target_orders_table_name} (
            order_id, store_id, store_name, store_status, store_own_user_id, store_own_user_name, 
            store_own_user_tel, store_category, store_address, store_shop_no, store_province, 
            store_city, store_district, store_gps_name, store_gps_address, store_gps_longitude, 
            store_gps_latitude, is_signed, operator, operator_name, face_id, member_id, 
            store_create_date_ts, origin, day_order_seq, discount_rate, discount_type, discount,
            money_before_whole_discount, receivable, erase, small_change, total_no_discount,
            payed_total, pay_type, payment_channel, payment_scenarios, product_count,
            date_ts
        ) VALUES (
            {check_str_null_and_transform_to_sql_null(str(self.order_id))}, 
            {self.store_id}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_name))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_status))}, 
            {self.store_own_user_id}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_own_user_name))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_own_user_tel))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_category))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_address))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_shop_no))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_province))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_city))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_district))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_gps_name))}, 
            {check_str_null_and_transform_to_sql_null(str(self.store_gps_address))}, 
            {self.store_gps_longitude}, 
            {self.store_gps_latitude}, 
            {self.is_signed}, 
            {check_str_null_and_transform_to_sql_null(str(self.operator))}, 
            {check_str_null_and_transform_to_sql_null(str(self.operator_name))}, 
            {check_str_null_and_transform_to_sql_null(str(self.face_id))}, 
            {self.member_id}, 
            {self.store_create_date_ts}, 
            {check_str_null_and_transform_to_sql_null(str(self.origin))}, 
            {self.day_order_seq}, 
            {self.discount_rate}, 
            {self.discount_type}, 
            {self.discount},
            {self.money_before_whole_discount}, 
            {self.receivable}, 
            {self.erase}, 
            {self.small_change}, 
            {self.total_no_discount},
            {self.payed_total}, 
            {check_str_null_and_transform_to_sql_null(str(self.pay_type))}, 
            {check_str_null_and_transform_to_sql_null(str(self.payment_channel))}, 
            {check_str_null_and_transform_to_sql_null(str(self.payment_scenarios))}, 
            {self.product_count},
            {self.date_ts}
        );
        """
        return sql
    
class OrderDetailModel:
    def __init__(self, data:str):
        """ 
        从传入的字符串数据构建订单详情model
        此model质保函订单详情信息，包含订单中售卖的每件商品信息
        """
        ld = json.loads(data) # dict
        self.order_id = ld['orderID'] # 订单ID
        order_product_list = ld['product'] # 订单中售卖的商品列表，是一个list，每个元素是一个dict，包含单件商品信息
        self.product_list = [SingleProductSoldModel(self.order_id, product) for product in order_product_list] # 将订单中售卖的商品列表转换为SingleProductModel对象列表
        pass
    
    def to_csv(self, sep=','):
        """ 将订单详情model转换为csv字符串，字段顺序与建表语句一致 """
        csv_lines = ""
        for product in self.product_list:
            product_csv = product.to_csv(sep)
            csv_lines += product_csv + "\n"
        return csv_lines
    
    def generate_insert_sql(self):
        sql = f"INSERT IGNORE INTO {conf.target_order_detail_table_name} (order_id, name, count, unit_id, barcode, price_per, retail_price, trade_price, category_id) VALUES "
        for product in self.product_list:
            values = f"({check_str_null_and_transform_to_sql_null(str(product.order_id))}, {check_str_null_and_transform_to_sql_null(str(product.name))}, {product.count}, {check_str_null_and_transform_to_sql_null(str(product.unit_id))}, {check_str_null_and_transform_to_sql_null(str(product.barcode))}, {product.price_per}, {product.retail_price}, {product.trade_price}, {check_str_null_and_transform_to_sql_null(str(product.category_id))}), "
            sql += values
        sql = sql.rstrip(", ") + ";" # 去掉最后一个逗号和空格，添加分号结尾
        return sql

class SingleProductSoldModel:
    def __init__(self, order_id:str, product:dict):
        """ 
        从传入的字符串数据构建单件商品model
        此model质保函订单中售卖的单件商品信息
        """
        self.order_id = order_id # 订单ID
        self.name = product['name'] # 商品名称
        self.count = product['count'] # 商品数量
        self.unit_id = product['unitID'] # 商品单位ID
        self.barcode = product['barcode'] # 商品条形码
        self.price_per = product['pricePer'] # 商品单价
        self.retail_price = product['retailPrice'] # 商品零售价
        self.trade_price = product['tradePrice'] # 商品折扣价
        self.category_id = product['categoryID'] # 商品类别ID
        pass       
    
    def to_csv(self, sep=','):
        """ 将单件商品model转换为csv字符串，字段顺序与建表语句一致 """
        return sep.join([
            self.order_id,
            self.name,
            str(self.count),
            self.unit_id,
            self.barcode,
            str(self.price_per),
            str(self.retail_price),
            str(self.trade_price),
            self.category_id
        ])
    
if __name__ == "__main__":
    jsonStr = '{"discountRate":0.9,"storeShopNo":"None","dayOrderSeq":1,"storeDistrict":"朝阳区","isSigned":1,"storeProvince":"北京市","origin":"app","storeGPSLongitude":"116.481488","discount":10,"storeID":1001,"productCount":3,"operatorName":"张三","operator":"10001","storeStatus":"营业中","storeOwnUserTel":"13800000000","payType":"微信支付","discountType":"会员折扣","storeName":"测试店铺","storeOwnUserName":"李四","dateTS":1622520000000,"smallChange":0.5,"storeGPSName":"测试店铺GPS名称","erase":0,"storeGPSAddress":"测试店铺GPS地址","orderID":"ORD1234567890","moneyBeforeWholeDiscount":100,"storeCategory":"餐饮","receivable":90,"faceID":"FACE1234567890","storeOwnUserId":20001,"paymentChannel":"线上","paymentScenarios":"正常支付","storeAddress":"测试店铺地址","totalNoDiscount":110,"payedTotal":90,"storeGPSLatitude":"39.990475","storeCreateDateTS":1609459200000,"storeCity":"北京市","memberID":30001,"product":[{"name":"商品A","count":2,"unitID":"U01","barcode":"1234567890","pricePer":10,"retailPrice":12,"tradePrice":8,"categoryID":"CAT01"},{"name":"商品B","count":1,"unitID":"U02","barcode":"0987654321","pricePer":20,"retailPrice":24,"tradePrice":16,"categoryID":"CAT02"}]}'
    print(type(jsonStr))
    order = OrderModel(jsonStr)
    print("订单信息\n")
    print(order.to_csv())
    # print(order.generate_insert_sql())

    detail = OrderDetailModel(jsonStr)  # 通过模型暂存数据，最终是为了转出csv和sql
    # print([vars(p) for p in detail.product_list])
    print("\n订单详情信息")
    print(detail.to_csv())
    print(detail.generate_insert_sql())
