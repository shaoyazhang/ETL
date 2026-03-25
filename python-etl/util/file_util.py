import os


def get_dir_files_list(path, recursive=False):
    """
    获取指定路径下所有的文件名（绝对路径）
    :param path: 指定路径
    :param recurseive: 是否递归的获取子目录下的文件名
    :return: 获取到的文件名列表
    """
    dir_names = os.listdir(path)
    files = []
    for dir_name in dir_names:
        ''' 
        os.path.join() 会根据当前操作系统，自动用正确的路径分隔符
        '''
        absolute_path = os.path.join(path, dir_name)
        if not os.path.isdir(absolute_path):
            files.append(absolute_path)
        else:
            if recursive:
                files += get_dir_files_list(absolute_path, recursive)
                
    return files


def get_new_by_compare_lists(a_list, b_list):
    ''' 
    接收两个列表对比他们的差异
    a_list: 接收的是从指定目录中获取的文件名
    b_list: 接收的是从元数据表中获取的处理过的文件名
    return: 两个列表差异
    '''
    # 在a_list且不在b_list中的元素
    return list(set(a_list) - set(b_list))

def get_new_by_compare_lists1(a_list, b_list):
    result = []
    for a in a_list:
        if a not in b_list:
            result.append(a)
            
    return result