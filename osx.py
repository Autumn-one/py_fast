from os import walk, listdir, path
from pathlib import Path
from pathx import *  # 导入所有的路径增强函数
from walkx import *  # 导入所有的递归访问文件夹的方法
from pprint import *  # 导入所有的pprint的方法
from shutil import * # 导入文件的高级操作部分


def get_dirs(path_str=None, nopath=False):
    """
    返回给定路径的直接子文件夹
    nopath 表示是否输出完整的路径
    """
    dirs = []  # 存放最终结果的文件列表

    if not path_str:
        path_str = cwd()

    for item in listdir(path_str):
        item_path = Path(path_str, item)
        if is_dir(item_path):
            final_path = item if nopath else str(item_path)
            dirs.append(final_path)

    return dirs


def get_files(path_str, extension="", *, nopath=False):
    """
    返回给定路径的直接子文件
    extension 表示后缀名不带点
    nopath表示是狗返回完整路径,注意不一定是绝对路径
    """
    files = []  # 存放最终结果的文件列表

    if not path_str:
        path_str = cwd()

    if extension:
        extension = "." + extension

    for item in listdir(path_str):
        item_path = Path(path_str, item)
        if is_file(item_path) and item.endswith(extension):
            final_path = item if nopath else str(item_path)
            files.append(final_path)

    return files


def get_all(path_str, classify=False, nopath=False):
    """
    返回给定路径的直接文件列表和文件夹列表
    默认返回一个列表包含所有的文件和文件夹
    classify为True就返回两个列表,一个是文件列表一个是目录列表,默认的False表示返回一个列表
    """
    files = []
    dirs = []

    if not path_str:
        path_str = cwd()

    for item in listdir(path_str):
        item_path = Path(path_str, item)
        final_name = item if nopath else str(item_path)
        if is_file(item_path):
            files.append(final_name)
        else:
            dirs.append(final_name)

    if classify:
        return files, dirs
    else:
        return [*files, *dirs]
