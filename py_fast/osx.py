from os import walk, listdir, path
from pathlib import Path
from .pathx import *  # 导入所有的路径增强函数
from .walkx import *  # 导入所有的递归访问文件夹的方法
import shutil  # 导入文件的高级操作部分
import json
import ast
from . import clipx
from pprint import pformat
import copy as cp
from .easyx import *
import os
from typing import Tuple, List, Optional


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


def get_files(path_str=None, extension="", *, nopath=False, glob=None):
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
        files = walk_files(path_str, nopath=nopath, glob=glob)
    else:
        for item in listdir(path_str):
            item_path = Path(path_str, item)
            if is_file(item_path) and item.endswith(extension):
                final_path = item if nopath else str(item_path)
                files.append(final_path)

    return files


def get_all(path_str=None, classify=False, nopath=False):
    """
    返回给定路径的直接文件列表和文件夹列表
    默认返回一个列表包含所有的文件和文件夹
    classify为True就返回两个列表,一个是文件列表一个是目录列表,默认的False表示返回一个列表
    """
    files = []
    dirs = []

    if path_str is None:
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
def new_dir(path_str, recur=True, mode=511):
    """
    创建一个文件夹, 支持递归创建
    path_str 是一个文件夹得路径, 默认会递归创建所有中间文件夹
    recur 是否递归创建中间文件夹, 默认 True
    """
    path_str = to_abs(path_str)
    if recur:
        os.makedirs(path_str, mode=mode)
    else:
        os.mkdir(path_str, mode=mode)


def new_dirs(*args, recur=True):
    """
    创建多个文件夹
    可以这样写
    new_dirs("目录一","目录二","目录三")
    也可以这样写
    new_dirs(["目录一","目录二","目录三"])
    """
    if len(args) == 1:
        for i in args[0]:
            new_dir(i, recur=recur)
    else:
        for i in args:
            new_dir(i, recur=recur)


"""
os.makedirs(name, mode=511, exist_ok=False)
递归目录创建函数。与 mkdir() 类似，但会自动创建到达最后一级目录所需要的中间目录。

mode 参数会传递给 mkdir()，用来创建最后一级目录，对于该参数的解释，请参阅 mkdir() 中的描述。要设置某些新建的父目录的权限，可以在调用 makedirs() 之前设置 umask。现有父目录的权限不会更改。
"""


def new_file(path_str, content=None, encoding="utf8", *, recur=True):
    """
    创建一个文件
    file_name 文件名称或者一个文件路径
    content是一个可选的要假如文件的字符串内容
    encoding是文字编码
    recur 是否递归创建中间需要的所有目录
    """
    path_str = to_abs(path_str)

    base_path = dirname(path_str)

    if not_exist(base_path) and recur:
        new_dir(base_path)

    if content:
        Path(path_str).write_text(content, encoding=encoding)
    else:
        Path(path_str).touch()


def new_files(*args):
    """
    创建多个文件, 可以直接写文件夹创建多个空的文件, 或者创建得时候指定初始内容
    new_files("1.txt","2.txt","3.txt")
    new_files(("1.txt","内容1"),("2.txt","内容2"),("3.txt","内容3"))
    """
    for i in args:
        if isinstance(i, list) or isinstance(i, tuple):
            new_file(i[0], i[1])
        else:
            new_file(i[0])


def new(name: str, content: str = None):
    """
    创建目录或者文件, 默认带后缀就是文件不带后缀就是目录
    name是文件或者目录名字
    content是内容
    """
    if is_in(".", basename(name)) or content:  # 如果存在第二个 content 参数或者名字带点都认为是一个文件
        new_file(name, content)
    else:
        new_dir(name)


def news(*args):
    """
    创建多个文件或者目录
    news("1.txt","2.txt")
    news("abc",("1.txt","内容"),"2.txt")
    """
    for i in args:
        if type(i) == list or type(i) == tuple:
            new_file(i[0], i[1])
        elif "." in i:
            new_file(i)
        else:
            new_dir(i)


def remove(file_dir=None, glob=None):
    """
    删除文件或者文件夹
    file_dir 文件或目录名称或路径
    """
    if file_dir is None and not glob is None:
        for p in walk_all(glob=glob):
            if is_file(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
        return

    if is_file(file_dir):
        os.remove(file_dir)
    else:
        shutil.rmtree(file_dir)


# 删除文件 只能删除文件 删除目录直接报错
remove_file = os.remove

# 删除文件夹
remove_dir = shutil.rmtree

stat = os.stat


def read(file_name, encoding="utf8", newline=None):
    """
    读取文件内容, 只能读文本, 不能读二进制
    """
    with open(file_name, encoding=encoding, newline=newline) as f:
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
    return pformat(obj)


def copy(src=None, dst=None, *, follow_symlinks=True, ignore=None, glob=None):
    """
    用于复制变量,文件或者文件夹的函数, 将src拷贝到dst
    如果只传入了一个参数就是浅复制变量
    src 是一个文件或者目录, 路径字符串或者路径对象都行
    dst 是一个文件或目录,如果是文件就是拷贝到指定的文件路径如果是目录且src不是目录就是拷贝到目录下面,如果是目录且src也是目录就是复制到路径
    follow_symlinks 和 shutil.copy 的同名参数一致的意思
    ignore 表示一个 glob 风格的忽略那些文件和目录, 注意这个参数可以提供一个或者多个,一个可以直接给出字符串, 多个用字符串元祖即可
    glob 只在 src 是目录而时候有用, 表示通过通配符匹配来复制所有匹配到的文件到指定目录, 和ignore参数互斥
    """
    if not src is None and dst is None:
        return cp.copy(src)

    if src is None or src == '.':
        # 如果 src 是None 或者 src是.
        src = cwd()

    dst = to_abs(dst)

    if is_file(src):  # 如果复制文件, 查看dst 目标路径中是否有不存在的目录,有就创建好在复制
        base_path = dirname(dst)
        if not is_exist(base_path):
            new_dir(base_path)
        return shutil.copy(src, dst, follow_symlinks=follow_symlinks)
    else:
        if type(ignore) == str:
            ignore = (ignore,)

        if glob:  # 如果有通配符选项则是复制目录下指定通配符的文件到指定文件夹
            # 先判断目标文件夹存不存在;,如果不存在就创建
            not is_exist(dst) and new_dir(dst)

            files = walk_files(src, glob=glob)
            for file in files:
                shutil.copy(file, dst)

        else:
            return shutil.copytree(src, dst, symlinks=not follow_symlinks,
                                   ignore=shutil.ignore_patterns(*ignore) if ignore else None)


copy2 = shutil.copy2

deep_copy = cp.deepcopy  # 深度复制变量

copy_file = shutil.copy
copy_dir = shutil.copytree


def openx(*args, **kws):
    """
    默认utf8编码的open函数
    """
    return open(*args, **{**kws, "encoding": "utf8"})


def cmd(cmd_str):
    """
    该方法接受一个cmd命令字符串, 执行这条命令
    """
    return os.popen(cmd_str, mode="r", buffering=-1)


def rename(src, name):
    """
    找到一个文件或者目录进行重命名
    name 只能是一个文件名或者一个目录名
    """
    dir_path = dirname(src)
    os.rename(src, Path(dir_path) / name)


def rename_file(src, name):
    """
    重命名一个文件, 对文件夹重命名会出错
    """
    if is_file(src):
        rename(src, name)
    else:
        raise Exception(f"{src}不是一个文件或者不存在")


def rename_dir(src, name):
    """
    重命名一个目录, 对非目录重命名会报错

    """
    if is_dir(src):
        rename(src, name)
    else:
        raise Exception(f"{src}不是一个文件或者不存在")

def count_files(directory: str, extension: str) -> int:
    """
    此函数用于统计指定文件夹及其子文件夹中，指定后缀的文件数量
    :param directory: 传入的目录路径，应为字符串
    :param extension: 需要统计的文件后缀，如 ".txt", ".csv", ".jpg" 等
    :return: 返回指定后缀的文件数量
    """
    count = 0  # 初始化数量为0
    # 使用os.walk遍历directory目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 在文件中,如果文件的后缀名与参数extension相同，计数器加一
        for file in files:
            if file.endswith(extension):
                count += 1
    # 返回数量
    return count


def change_file_creation_time(filename: str, new_time: str) -> None:
    """
    修改指定文件的创建时间
    :param filename: 需要修改的文件名
    :param new_time: 新的创建时间，格式为"YYYY-MM-DD HH:MM:SS"
    """
    ctime = time.mktime(time.strptime(new_time, "%Y-%m-%d %H:%M:%S"))  # 转换为时间戳

    cfile = ctypes.CDLL('Kernel32.dll')
    handle = cfile.CreateFileW(filename, ctypes.c_uint32(0x10000000), 0, None, 3, 0x80, None)
    if handle == -1:  # 如果返回-1，那么代表创建文件句柄失败。
        raise ctypes.WinError()
    ctime_low = ctypes.c_uint32(int(ctime) & 0xFFFFFFFF)  # 取低位
    ctime_high = ctypes.c_uint32(int(ctime) >> 32)  # 取高位
    cfile.SetFileTime(handle, ctypes.byref(ctime_low), None, None)   # 设置文件创建时间
    cfile.CloseHandle(handle)


def change_file_modification_time(filename: str, new_time: str):
    """
    修改指定文件的修改时间
    :param filename: 需要修改的文件名
    :param new_time: 新的修改时间，格式为"YYYY-MM-DD HH:MM:SS"
    """
    mtime = time.mktime(time.strptime(new_time, "%Y-%m-%d %H:%M:%S"))  #转换为时间戳
    mtime_low = ctypes.c_uint32(int(mtime) & 0xFFFFFFFF)  #低位
    mtime_high = ctypes.c_uint32(int(mtime) >> 32)  #高位

    cfile = ctypes.CDLL('Kernel32.dll')  #加载库
    #创建文件句柄
    handle = cfile.CreateFileW(filename, ctypes.c_uint32(0x10000000), 0, None, 3, 0x80, None)
    if handle == -1:
        raise ctypes.WinError()

    #设定修改时间
    cfile.SetFileTime(handle, None, None, ctypes.byref(ctime_low))
    cfile.CloseHandle(handle)  #关闭句柄


def rename_files(directory: str, prefix: str):
    """
    批量修改指定文件夹中的所有文件名
    :param directory: 需要修改的文件夹路径
    :param prefix: 新的文件名前缀
    """
    for filename in os.listdir(directory):
        # 组合出新的文件名
        new_filename = prefix + '_' + os.path.basename(filename)
        # 获取原文件的完整路径
        old_file = os.path.join(directory, filename)
        # 组合出修改后的文件名路径
        new_file = os.path.join(directory, new_filename)
        # 重命名文件
        os.rename(old_file, new_file)