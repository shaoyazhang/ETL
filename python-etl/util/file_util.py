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

