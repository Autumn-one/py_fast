"""
pyinstaller 相关的工具函数
"""
from os import path
from pathlib import Path
import time, sys, os
from win32com.client import Dispatch
import __main__
def get_log_time():
    """获取当前的时间"""
    return time.strftime("%Y年%m月%d日 %I时 %M分 %S秒",time.localtime())

def get_source_path():
    """获取真实的执行文件的路径"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        file_path = Path(sys.executable)
    else:
        if hasattr(__main__,"__file__"):
            file_path = Path(__main__.__file__)
        else:
            file_path = Path(__file__)
    return file_path

def get_real_path(pstr):
    """得到LNK快捷文件和软链接的真实路径, 返回一个字符串"""
    final_path = None
    if pstr.endswith(".lnk"):
        # 如果是快捷方式那么就读取快捷方式的真实路径
        shell = Dispatch("WScript.Shell")
        final_path =  shell.CreateShortCut(pstr).TargetPath
    elif path.islink(pstr):
        # 如果是软链接那么也获取真实的路径
        try:
            final_path = os.readlink(pstr)
        except Exception:
            return pstr
    else:
        final_path = pstr

    return final_path

def is_frozen():
    """判断当前是否是单exe文件环境"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return True
    else:
        return False


__all__ = ('get_log_time', 'get_source_path', 'get_real_path', 'is_frozen')
