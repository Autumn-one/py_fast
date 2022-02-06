from os import walk, listdir, path
from pathlib import Path
from pathx import *  # 导入所有的路径增强函数
from walkx import *  # 导入所有的递归访问文件夹的方法
from pprint import *  # 导入所有的pprint的方法
from shutil import *  # 导入文件的高级操作部分
import json
import ast


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


# 创建一个目录
new_dir = os.mkdir


def new_file(file_name, content=None, encoding="utf8"):
    """
    创建一个文件
    file_name 文件名称或者一个文件路径
    content是一个可选的要假如文件的字符串内容
    encoding是文字编码
    """
    if content:
        Path(file_name).write_text(content, encoding=encoding)
    else:
        Path(file_name).touch()


def remove(file_dir):
    """
    删除文件或者文件夹
    file_dir 文件或目录名称或路径
    """
    if is_file(file_dir):
        os.remove(file_dir)
    else:
        rmtree(file_dir)


# 删除文件
remove_file = os.remove

# 删除文件夹
remove_dir = rmtree

stat = os.stat


def read(file_name, encoding="utf8"):
    """
    读取文件内容
    """
    with open(file_name, encoding=encoding) as f:
        return f.read()


def write(file_name, content, *, append=True, encoding="utf8"):
    """
    写入文件内容
    append如果为True则是追加写入 False则是覆写
    """
    mode = "a" if append else "w"  # 写入的模式是追加还是覆写
    with open(file_name, mode, encoding=encoding) as f:
        f.write(content)


def read_json(path_str):
    """
    读取json文件返回的是一个py对象
    """
    with open(path_str, encoding="utf8") as f:
        return json.load(f)


def write_json(path_str, obj):
    """
    将py对象写入到json文件
    """
    with open(path_str, "w", encoding="utf8") as f:
        return json.dump(obj, f, check_circular=False)


def str2obj(s):
    """
    字符串转换成py对象并返回
    """
    return ast.literal_eval(s)


def obj2str(obj):
    """
    py对象转换成字符串
    """
    return json.dumps(obj, check_circular=False)


copy_dir = copytree
