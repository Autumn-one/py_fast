from os import walk, listdir, path
from pathlib import Path
from pathx import *  # 导入所有的路径增强函数
from walkx import *  # 导入所有的递归访问文件夹的方法
import shutil  # 导入文件的高级操作部分
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


def get_files(path_str, extension="", *, nopath=False, glob=None):
    """
    返回给定路径的直接子文件
    extension 表示后缀名不带点
    nopath表示是狗返回完整路径,注意不一定是绝对路径
    glob 表示使用通配符来匹配文件
    """
    files = []  # 存放最终结果的文件列表

    if not path_str:
        path_str = cwd()

    if extension:
        extension = "." + extension

    if glob:
        files = walk_files(path_str,nopath=nopath,glob=glob)
    else:
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

# 创建目录或者文件, 带后缀就是文件不带后缀就是目录
def new(name: str, content: str = None):
    if "." in name or content: # 如果存在第二个 content 参数或者名字带点都认为是一个文件
        new_file(name, content)
    else:
        new_dir(name)


def remove(file_dir):
    """
    删除文件或者文件夹
    file_dir 文件或目录名称或路径
    """
    if is_file(file_dir):
        os.remove(file_dir)
    else:
        shutil.rmtree(file_dir)


# 删除文件
remove_file = os.remove

# 删除文件夹
remove_dir = shutil.rmtree

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


def copy(src, dst, *, follow_symlinks=True, ignore=None, glob=None):
    """
    用于复制文件或者文件夹的函数, 将src拷贝到dst
    src 是一个文件或者目录, 路径字符串或者路径对象都行
    dst 是一个文件或目录,如果是文件就是拷贝到指定的文件路径如果是目录且src不是目录就是拷贝到目录下面,如果是目录且src也是目录就是复制到路径
    follow_symlinks 和 shutil.copy 的同名参数一致的意思
    ignore 表示一个 glob 风格的忽略那些文件和目录, 注意这个参数可以提供一个或者多个,一个可以直接给出字符串, 多个用字符串元祖即可
    glob 只在 src 是目录而时候有用, 表示通过通配符匹配来复制所有匹配到的文件到指定目录, 和ignore参数互斥
    """
    if is_file(src):
        return shutil.copy(src, dst, follow_symlinks=follow_symlinks)
    else:

        if type(ignore) == str:
            ignore = (ignore,)

        if glob: # 如果有通配符选项则是复制目录下指定通配符的文件到指定文件夹
            files = walk_files(src,glob=glob)
            for file in files:
                shutil.copy(file,dst)

        else:
            return shutil.copytree(src, dst, symlinks=not follow_symlinks, ignore=shutil.ignore_patterns(*ignore) if ignore else None)

copy2 = shutil.copy2

copy_file = shutil.copy
copy_dir = shutil.copytree


def openx(*args,**kws):
    """
    默认utf8编码的open函数
    """
    return open(*args,**{**kws,"encoding":"utf8"})