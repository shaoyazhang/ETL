""" 
字符串工具类
"""

def check_null(data):
    """
    检查传入的字符串，是否为无意义内容，如果是就返回True, 否则返回False
    无意义：字符串为空字符串，内容是None, null, undeined 
    data: 传入的被检查的字符串内容
    return: 如果data是无意义内容，返回True，否则返回False
    """
    
    if not data:
        # data这个对象，如果是python中的None, 直接返回无意义
        return True
    
    """ 
    None在if判断中，表示False
    if None == if False
    
    如果data是None
    if not data == if not False = 会进入if循环
    """
    
    # 统一转小写，避免大小写问题
    # 调用字符串的lower方法
    data = data.lower().strip()
    # 判断是否无意义
    if data == "none" or data == "" or data == "null" or data == "undefined":
        return True
    return False


def check_str_null_and_transform_to_sql_null(data):
    """
    检查字符串是否无意义，如果是无意义，就转换成sql中的null，否则返回原字符串
    data: 传入的被检查的字符串内容
    return: 如果data是无意义内容，返回sql中的null，否则返回原字符串
    """
    if check_null(str(data)):
        # 内容无意义，返回sql中的Null
        return "NULL"
    else:
        # 内容有意义，返回'内容本身'
        return f"'{data}'"



