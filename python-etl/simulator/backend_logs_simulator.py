import datetime
import os
import random
import time

single_log_lines = 1024 # 一个logs文件生成多少行数据
generate_files = 5 # 生成多少个logs文件

output_path = 'D:\\Pythons_studies\\logs\\logs\\'

log_level_array = ['WARN', 'WARN', 'WARN', 'INFO', 'INFO']

backend_files_name = ['barcode_service.py', 'order_service.py', 'payment_service.py', 'user_service.py']

# 日志消息模板
log_messages = {
    'INFO': [
        'Processing user request',
        'Database connection established',
        'Order processed successfully',
        'Payment transaction completed',
        'User authentication successful',
        'Data synchronization started',
        'Cache updated',
        'Service health check passed'
    ],
    'WARN': [
        'High memory usage detected',
        'Slow response time',
        'Database query timeout',
        'Invalid input parameters',
        'Service temporarily unavailable',
        'Rate limit exceeded',
        'Deprecated API usage',
        'Configuration warning'
    ]
}

provinces_and_cities = {
    '北京': ['北京市'],
    '上海': ['上海市'],
    '广东': ['广州市', '深圳市', '珠海市', '佛山市'],
    '浙江': ['杭州市', '宁波市', '温州市'],
    '江苏': ['南京市', '无锡市', '苏州市']
}

response_time_range = (10, 2000)  # ms

headers = ['日志时间', '日志级别', '代码模块', '接口响应时间', '调用者省份', '调用者城市', '日志信息']

def generate_log_line():
    """生成单行日志，按指定格式"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    level = random.choice(log_level_array)
    module = random.choice(backend_files_name)
    response_time = random.randint(*response_time_range)
    province = random.choice(list(provinces_and_cities.keys()))
    city = random.choice(provinces_and_cities[province])
    message = random.choice(log_messages[level])

    # 使用制表符作为分隔符，便于导入和阅读
    log_line = f"{timestamp}\t{level}\t{module}\t{response_time}ms\t{province}\t{city}\t{message}\n"
    return log_line

def generate_log_file(file_index):
    """生成单个日志文件"""
    file_name = f"{output_path}{file_index}.log"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    with open(file_name, 'w', encoding='utf-8') as f:
        # 写入表头
        f.write('\t'.join(headers) + '\n')
        for _ in range(single_log_lines):
            log_line = generate_log_line()
            f.write(log_line)
            # 模拟时间间隔
            time.sleep(random.uniform(0.001, 0.01))  # 随机延迟
    
    print(f"Generated log file: {file_name}")

if __name__ == "__main__":
    print("Starting backend logs simulator...")
    
    for i in range(1, generate_files + 1):
        generate_log_file(i)
    
    print("All log files generated successfully!")

