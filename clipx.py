# 这是一个用于控制系统剪切板的库, 不论是文字还是文件文件夹都可以做到 复制粘贴

import pyperclip as clip
import win32clipboard
from ctypes import *
from pathx import *


class DROPFILES(Structure):
    _fields_ = [
        ("pFiles", c_uint),
        ("x", c_long),
        ("y", c_long),
        ("fNC", c_int),
        ("fWide", c_bool),
    ]


pDropFiles = DROPFILES()
pDropFiles.pFiles = sizeof(DROPFILES)
pDropFiles.fWide = True
matedata = bytes(pDropFiles)


def setClipboardFiles(paths):
    files = ("\0".join(paths)).replace("/", "\\")
    data = files.encode("U16")[2:]+b"\0\0"
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32clipboard.CF_HDROP, matedata+data)
    finally:
        win32clipboard.CloseClipboard()


def setClipboardFile(file):
    setClipboardFiles([file])


def readClipboardFilePaths():
    win32clipboard.OpenClipboard()
    # paths = None
    try:
        return win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
    finally:
        win32clipboard.CloseClipboard()



def copy(copy_type = "", copy_res = None):
    """
    如果传入一个文本参数则是直接将这个文本添加到剪切板
    有多种调用方式:
    copy("直接复制一些文字到系统剪切板")
    copy("text","直接复制一些文字到系统剪切板")
    copy("file","d:/1.txt") 复制文件或者文件夹到系统的剪切板
    copy("file",["d:/1.txt","d:/aaa"]) 复制多个文件或者文件夹到系统的剪切板
    """
    type_set = { # 拷贝到剪切板的类型
        "text", # 普通文本
        "file", # 文件或者文件夹也可以是多个我恩件或者文件夹, 用一个序列装一下就好了
    }

    if type(copy_type) == str and not copy_res: # 如果只传入了一个字符串, 没有传入第二个参数就直接复制字符串到剪切板
        copy_text = copy_type
        clip.copy(copy_text)
        return None

    if copy_type in type_set and copy_res:
        if copy_type == "text":
            copy_text = copy_type
            clip.copy(copy_text)
        elif type(copy_res) == str: # 如果是单个文本说明是一个url
            if not is_exist(copy_res):
                raise Exception(f"路径:{copy_res} 不存在")
            else:
                setClipboardFile(copy_res)
        else: # 如果不是一个字符串说明是多个文件
            for p in copy_res:
                if not is_exist(p):
                    raise Exception(f"路径:{copy_res} 不存在")
            setClipboardFiles(copy_res)

        return None

    raise Exception(f"参数错误!")


def paste():
    """
    返回两个值, 第一个为值的类型,只有三种可能一个是 text 或者 file None表示没有东西
    第二个值表示实际的结果;,如果是简单的文本就是一个字符串;,如果是一个非简单文本将会是一个元组,表示所有的文件路径,哪怕只有一个文件也是一个元组
    """
    clip_con = clip.paste()

    if clip_con:
        return "text", clip_con
    else:
        try:
            clip_con = readClipboardFilePaths()
            return "file", clip_con
        except Exception as e:
            return None, e










