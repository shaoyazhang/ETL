import time

def ts10_to_date_str(ts, format_str="%Y-%m-%d %H:%M:%S"):
    """

    Args:
        ts (_type_): 10位时间戳
        format_str (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
        return: 时间日期字符串
    """
    return time.strftime(format_str, time.localtime(ts))


def ts13_to_date_str(ts, format_str="%Y-%m-%d %H:%M:%S"):
    ''' 
    ts (_type_): 13位时间戳
    format_str (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
    return: 时间日期字符串
    '''
    
    ts10 = int(ts/1000)
    return ts10_to_date_str(ts10, format_str)