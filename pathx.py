from os import path
import os

is_abs = path.isabs # 判断是否是绝对路径
is_file = path.isfile # 判断是否是文件
is_dir = path.isdir # 判断是否是文件夹
is_link = is_symlink = path.islink # 重命名判断软链接的方法
is_exist = path.exists # 判断路径是否存在

def cwd(path_str=None):
    """
    获取或者设置当前的工作目录
    如果给出了 path_str 那么就是设置 没有给出就是获取当前的工作目录
    """
    if path_str:
        return os.chdir(path_str)
    else:
        return os.getcwd()


