import ntpath
from os import walk, path
from pathlib import Path
from osx import *


def walk_files(path_str=None, extension="", *, nopath=False, followlinks=False, glob=None):
    """
        返回包含指定路径下的所有文件列表
        extension 表示文件后缀名,不带. 如果传入表示只返回相应后缀的文件
        nopath 代表是否携带路径,如果只是想返回文件名那么将该选项设置成 True
        followlinks 如果为False 则遇到符号链接直接返回符号链接的名称不会继续根据符号链接地址找到真实文件或文件夹
        glob 表示启用通配符匹配文文件,是一个字符串
    """
    files = []  # 放所有文件的列表

    # 如果没有给出路径,那么就是当前文件夹
    if not path_str:
        path_str = cwd()
    # 对extendsion 添加点,如果为空就不添加点
    if extension:
        extension = "." + extension

    if glob:
        files = [
            path.basename(str(file_path)) if nopath else str(file_path)
            for file_path in Path(path_str).glob(glob)
            if is_file(file_path) and str(file_path).endswith(extension)
        ]
    else:
        for curr_dir, _, file_list in walk(path_str, followlinks=followlinks):
            files += [
                file_name if nopath else str(Path(curr_dir, file_name))
                for file_name in file_list
                if file_name.endswith(extension)
            ]

    return files


def walk_dirs(path_str=None, *, nopath=False, followlinks=False, glob=None):
    """
    返回包含指定路径下的所有目录列表
    nopath 代表是否携带路径,如果只是想返回文件名那么将该选项设置成 True
    followlinks 如果为False 则遇到符号链接直接返回符号链接的名称不会继续根据符号链接地址找到真实文件或文件夹
    glob 表示启用通配符匹配文文件,是一个字符串
    """
    dirs = []

    # 如果path_str没有传那么就相对于当前的目录做遍历
    if not path_str:
        path_str = cwd()

    # 如果glob传了那么使用 Path 的glob功能
    if glob:
        dirs = [
            path.basename(dir_name) if nopath else str(dir_name)
            for dir_name in Path(path_str).glob(glob)  # 使用 glob获取所有的文件夹和文件
            if is_dir(dir_name)  # 只返回目录
        ]
    else:
        for curr_dir, dir_list, _ in walk(path_str, followlinks=followlinks):
            dirs += [
                dir_name if nopath else str(Path(curr_dir, dir_name))
                for dir_name in dir_list
            ]

    return dirs


def walk_all(path_str=None, *, classify=False, nopath=False, followlinks=False, glob=None):
    """
    返回路径 path_str 下的所有后代文件和文件夹
    classify 参数表示是否对文件和文件夹分类,如果为True则返回两个列表,一个是文件列表一个是文件夹列表,如果是False那么返回一个列表包含文件和文件夹
    """
    if not path_str:
        path_str = cwd()

    files = []  # 专门装文件的
    dirs = []  # 专门装文件夹的

    if glob:
        for curr_path in Path(path_str).glob(glob):
            final_file = path.basename(curr_path) if nopath else str(curr_path)
            if is_file(curr_path):
                files.append(final_file)
            else:
                dir.append(final_file)
    else:
        for curr_dir, dir_list, file_list in walk(path_str, followlinks=followlinks):
            if nopath:
                files += file_list
                dirs += dir_list
            else:
                files += [str(Path(curr_dir, i)) for i in file_list]
                dirs += [str(Path(curr_dir, i)) for i in dir_list]

    if classify:
        return files, dirs
    else:
        return [*files, *dirs]
