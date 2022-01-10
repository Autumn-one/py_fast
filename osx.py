from os import walk, listdir, path
from pathlib import Path


def walk_files(path_str=".", extension="", *, nopath=False, followlinks=False):
    """
        返回包含指定路径下的所有文件列表
        extension 表示文件后缀名,不带. 如果传入表示只返回相应后缀的文件
        nopath 代表是否携带路径,如果只是想返回文件名那么将该选项设置成 True
    """
    files = []  # 放所有文件的列表

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