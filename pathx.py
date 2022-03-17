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


def dirname(path_str):
    """
    传入一个路径返回这个目标路径的上一个文件夹路径
    """
    # 判断路径是否是以 / 或者 \ 结尾的如果是去掉在返回 path.dirname 的处理结果

    if path_str.endswith(r"/") or path_str.endswith("\\"):
        path_str = path_str[0:len(path_str)-1]
    return path.dirname(path_str)


def basename(path_str):
    """
    传入一个路径返回这个目录路径指向的那个文件或者文件夹
    """
    if path_str.endswith(r"/") or path_str.endswith("\\"):
        path_str = path_str[0:len(path_str)-1]
    return path.basename(path_str)

