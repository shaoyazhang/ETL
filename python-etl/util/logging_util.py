import logging
from config.project_config import log_root_path, log_filename, level

class Logging():
    
    def __init__(self, level=20):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)


      
def init_logger():
    logger = Logging(level).logger
    
    # 避免重复输出日志
    # 判断这个logger是否之前已经添加过handler对象
    '''
    如果没有这个：
    因为python的换成机制
    第一次调用init_logger函数
    这时会添加stream_handler，file_handler
    第二次调用时，因为缓存了rootloger，所以会再次添加stream_handler，file_handler
    第三次调用时，缓存了rootlogger, 所以再次会添加filehandler streamhandler
    '''
    if logger.handlers:
        return logger
    
    
    # 构造handler对象
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        filename=log_root_path + log_filename,
        mode='a',
        encoding='utf-8'
    )
    
    fmt = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
    )
    
    stream_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    
    # 组合
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger
