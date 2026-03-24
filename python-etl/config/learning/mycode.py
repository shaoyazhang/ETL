from util.logging_util import init_logger


# import sys
# print(sys.path[0])


logger = init_logger()
# logger.info("测试 info")

'''
# 避免重复输出日志
# 判断这个logger是否之前已经添加过handler对象
if logger.handlers:
    return logger
'''

init_logger().info("测试 info1")
init_logger().info("测试 info2")
init_logger().info("测试 info3")