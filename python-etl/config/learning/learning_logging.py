import logging

# logging.getLogger().setLevel(10)    # 设置日志输出级别


'''
获取一个logging对象
logging可以输出到比如：控制台、文件中
logger对象的addHandler可以添加一个Handler对象
Handler对象就是里面记录了具体讲日志输出到什么地方
如果想要将日志输出到控制台，那么需要获得一个将日志输出到控制台的Handler对象
'''
logger = logging.getLogger()
'''通过logging.StreamHandler()就可以获取到一个将日志输出到控制台的Handler对象'''
stream_handler = logging.StreamHandler()

# 设置logger输出格式
'''
%(asctime)s 时间（自动生成）默认格式：YYYY-MM-DD HH:MM:SS
%(levelname)s 日志等级
%(filename)s 当前日志来自哪个文件
%(lineno)d 行号（注意 %d → 整数）
%(message)s 你写的日志内容
'''
fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s")
stream_handler.setFormatter(fmt)
'''通过logger对象的addHandler添加这个stream_handler，就可以将日志输出到控制台'''
logger.addHandler(stream_handler)

'''可以用logger对象设置而不是logging'''
logger.setLevel(10)
logger.debug('debug 日志输出') # 最啰嗦的模式，什么都可以说，级别10
logger.info('info 日志输出')   # 在代码的关键点输出，级别20
logger.warning('warning 日志输出') # 可能会出问题的地方，级别30
logger.error('error 日志输出') # 出问题 3306， “3306”，级别40
logger.fatal('fatal 日志输出') # 程序无法往后执行时，级别50
'''
每个级别都有对应的使用场景，场景必须合适
每个级别都有不同的重要程度
'''
# logging.debug('debug 日志输出') # 最啰嗦的模式，什么都可以说，级别10
# logging.info('info 日志输出')   # 在代码的关键点输出，级别20
# logging.warning('warning 日志输出') # 可能会出问题的地方，级别30
# logging.error('error 日志输出') # 出问题 3306， “3306”，级别40
# logging.fatal('fatal 日志输出') # 程序无法往后执行时，级别50


