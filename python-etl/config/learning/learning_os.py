import os

# 仅仅会返回文件名称,直接读取指定目录下的文件
# 如果需要读取指定目录下的子目录，这个代码是无法满足的
# files = os.listdir("D:/Pythons_studies/logs")
# print(files)
def read_dir(dir):
    results = []
    files = os.listdir(dir)
    for file in files:
        f = dir + '/' + file
        if os.path.isdir(f): # 判断指定的路径是文件还是目录
            # 当前file名是目录
            results += read_dir(f)
        else: 
            results.append(f)
    return results

# ret = read_dir("D:/Pythons_studies/logs")
# print(ret)   

''' 
os.path.exists(path)     # 存不存在
os.path.isfile(path)     # 是不是文件
os.path.isdir(path)      # 是不是目录
os.path.dirname(path)    # 父目录
os.path.basename(path)   # 文件名
os.path.join(a, b)       # 拼路径
os.path.abspath(path)    # 绝对路径
'''
print(os.getcwd()) # 获取的是当前执行路径/working directory
print(os.path.dirname(os.getcwd())) # 取一个路径的上一级目录