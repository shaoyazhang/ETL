import logging
from pathlib import Path

''' 
path = Path("D:/Pythons_studies/logs/test.log") 它只是表示一个路径，不要求这个路径真的存在。
最常用属性
    path.name      # test.log
    path.stem      # test
    path.suffix    # .log
    path.parent    # D:/Pythons_studies/logs
判断是否存在
    path.exists()   # 路径是否存在
    path.is_file()  # 是否是文件
    path.is_dir()   # 是否是目录
拼接路径
    log_path = Path("logs") / "test.log"
    这个 / 在 Path 里表示“拼接路径”。
创建目录
    Path("logs").mkdir(exist_ok=True)
    如果上级目录也可能不存在：
        Path("a/b/c").mkdir(parents=True, exist_ok=True)
        parents=True：上级目录不存在也一起创建
        exist_ok=True：目录已存在不报错
创建空文件
    Path("test.txt").touch(exist_ok=True)
读取文件
    text = Path("a.txt").read_text(encoding="utf-8")
写入文件
    Path("a.txt").write_text("hello", encoding="utf-8")
绝对路径
    path.resolve()
    Path("logs/test.log").resolve()
'''
def ensure_file_path(file_path):
    path = Path(file_path)
    ''' 
    parents=True 意思是如果上层目录不存在，也一起创建
    exist_ok=True 如果存在上级目录，不会报错
    '''
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


logger = logging.getLogger()

file_handler = logging.FileHandler(ensure_file_path(f"D:/Pythons_studies/logs/test.log"), encoding="utf-8")
file_handler1 = logging.FileHandler(ensure_file_path(f"D:/Pythons_studies/logs/test1.log"), encoding="utf-8")
stream_handler = logging.StreamHandler()

'''
%(asctime)s 时间（自动生成）默认格式：YYYY-MM-DD HH:MM:SS
%(levelname)s 日志等级
%(filename)s 当前日志来自哪个文件
%(lineno)d 行号（注意 %d → 整数）
%(message)s 你写的日志内容
'''
fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s")
file_handler.setFormatter(fmt)
file_handler1.setFormatter(fmt)
stream_handler.setFormatter(fmt)
'''通过logger对象的addHandler添加这个stream_handler，就可以将日志输出到控制台'''
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(file_handler1)

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


