from os import walk, listdir, path
from pathlib import Path
from pathx import * # 导入所有的路径增强函数
from walkx import * # 导入所有的递归访问文件夹的方法


def getFolders(pathStr):
    """返回给定路径的直接子文件夹"""
    return [*filter(
            lambda i: path.isdir(i),
            [*map(
                    lambda i: str(Path(pathStr, i)),
                    listdir(pathStr)
            )]
    )]


def getFiles(pathStr, extension=None):
    """返回给定路径的直接子文件"""
    files = [*filter(
            lambda i: path.isfile(i),
            [*map(
                    lambda i: str(Path(pathStr, i)),
                    listdir(pathStr)
            )]
    )]
    if extension:
        files = [*filter(
                lambda i: i.endswith(f".{extension}"),
                files
        )]
    return files


def getFilesAndFolders(pathStr):
    """返回给定路径的直接文件列表和文件夹列表"""
    filesAndFolders = listdir(pathStr)
    files = [*filter(
            lambda i: path.isfile(i),
            [*map(
                    lambda i: str(Path(pathStr, i)),
                    filesAndFolders
            )]
    )]
    folders = [*filter(
            lambda i: path.isdir(i),
            [*map(
                    lambda i: str(Path(pathStr, i)),
                    filesAndFolders
            )]
    )]
    return files, folders


def is_file(path_obj):
    """
    判断传入的路径是否是文件
    """
    return path.isfile(path_obj)

def is_dir(path_obj):
    """
    判断传入的路径是否是目录
    """
    return path.isdir(path_obj)


def is_exists(path_obj):
    """
    判断传入的路径是否存在
    """
    pass


def mkdir(path_obj):
    """
    新建一个目录
    """
    pass

def rmdir(path_obj):
    """
    删除一个目录
    """
    pass