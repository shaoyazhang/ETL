import time

print(time.time())  # 表示从1970年到现在过了多少秒
print(time.localtime(time.time()))
# 把时间日期格式化成字符串
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
print(time.strptime("2026-03-23 12:03:07", "%Y-%m-%d %H:%M:%S"))    # 把字符串按照格式解析成时间日期类型

