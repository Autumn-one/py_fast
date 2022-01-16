import ntpath
from os import walk,path
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
        files = [path.basename(str(file_path)) if nopath else str(file_path)
                 for file_path in Path(path_str).glob(glob)
                 if is_file(file_path) and str(file_path).endswith(extension)]
    else:
        for curr_dir, _, file_list in walk(path_str, followlinks=False):
            files += [file_name if nopath else str(Path(curr_dir, file_name))
                      for file_name in file_list
                      if file_name.endswith(extension)]

    return files


def walk_folders(path_str, *, followlinks=False):
    """返回包含指定路径下的所有文件夹列表"""
    folders = []

    for curr_dir, folder_list, _ in walk(path_str, followlinks=False):
        folders += [str(Path(curr_dir,folder)) for folder in folder_list]

    return folders


def walkFilesAndFolders(pathStr):
    """返回两个值，第一个是路径下所有文件路径列表，第二个是所有文件夹路径列表"""
    files = []
    folders = []
    for rootDir, folderList, fileList in walk(pathStr):
        files = [
            *files,
            *map(
                    lambda i: str(Path(rootDir, i)),
                    fileList
            )
        ]
        folders = [
            *folders,
            *map(
                    lambda i: str(Path(rootDir, i)),
                    folderList
            )
        ]
    return files, folders