from os import path
import os
from pathlib import Path
import re
from .sysx import *

is_abs = path.isabs # 判断是否是绝对路径
is_file = path.isfile # 判断是否是文件
is_dir = path.isdir # 判断是否是文件夹
is_link = is_symlink = path.islink # 重命名判断软链接的方法
is_exist = path.exists # 判断路径是否存在

__all__ = (
    "is_abs",
    "is_file",
    "is_dir",
    "is_link",
    "is_exist",
    "not_exist",
    "is_rel",
    "cwd",
    "dirname",
    "basename",
    "to_abs",
    "is_symlink"
)

def not_exist(*args, **kwargs):
    """
    判断路径是否不存在
    """
    return not is_exist(*args, **kwargs)

def is_rel(p):
    """
    判断路径是否是相对路径
    p 参数是一个 路径字符串或者 Path 对象
    """
    return not is_abs(p)

def cwd(path_str=None):
    """
    获取或者设置当前的工作目录
    如果给出了 path_str 那么就是设置 没有给出就是获取当前的工作目录
    """
    if path_str is None:
        return os.getcwd()
    else:
        if is_rel(path_str):
            path_str = Path(cwd()) / path_str
        return os.chdir(path_str)


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

def to_abs(path_arg):
    """
    传入一个路径字符串或者一个Path将一个路径转换成绝对路径, 返回路径字符串
    """
    if is_abs(path_arg):
        return path_arg

    path_str = str(Path(cwd()) / path_arg)

    path_list = re.split(r"[\\/]",path_str)
    path_list = [get_env(i) if i.startswith("%") and i.endswith("%") else i
                 for i in path_list]

    path_str = str(Path("/".join(path_list)))
    return path_str



