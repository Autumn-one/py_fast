"""pywin32 的封装"""

from os import path
from pathlib import Path
import time, traceback, sys, os, win32api, win32con, win32gui, win32process
from win32com.client import Dispatch
import __main__


def parse_argv():
    """格式化参数信息，返回一个参数对象"""
    args = sys.argv
    default_config = {
        "open"   : None,  # 打开模式
        "user"   : '1',  # 使用什么用户权限打开文件, 默认用户权限

        "copy"   : "fullpath",  # 复制模式，复制路径还是文件名
        "message": None,  # 是否显示提示
        "time"   : 1500,  # message 显示的时间

        "real"   : "yes",  # 遇到软连接或快捷方式是否追踪真实的地址
        "where"  : "select",  # 从哪里找路径
        "sound"  : None,  # 是否播放声音

        "cmd"    : "parent",  # 配置打开 cmd 的表现  parent 表示始终打开选中的上层目录 dir 表示如果当前就是一个目录那么久使用当前的，如果不是在回退到上一层
    }

    user = {  # 用户权限和数字的映射
        "user"   : "1",
        "admin"  : "3",
        "system" : "4",
        "trusted": "8",
    }

    arg_len = len(args)
    i = 1
    while i < arg_len:
        arg = args[i]  # 获取当前索引的参数
        next_index = i + 1
        next = args[next_index] if next_index < arg_len else None  # 获取下一个参数

        if arg == '-c':
            if next is not None and next in ('fullpath', 'name', 'fullname', 'ext', 'dir'):
                default_config['copy'] = next
                i += 2
        elif arg == '-o':
            if next is not None and next in ('dir', 'file', 'cmd'):
                default_config['open'] = next
                i += 2
        elif arg == '-cmd':
            if next is not None and next in ('parent', 'dir'):
                default_config['cmd'] = next
                i += 2
        elif arg == '-r':
            if next is not None and next in ('yes', 'no'):
                default_config['real'] = next
                i += 2
        elif arg == '-w':
            if next is not None and next in ('run', 'select'):
                default_config['where'] = next
                i += 2
        elif arg == '-m':
            default_config['message'] = True
            if next is not None and next.isdigit() and int(next) < 5000 and int(next) > 500:
                default_config['time'] = next
                i += 2
        elif arg == '-s':
            if next is not None:
                default_config['sound'] = next
                i += 2
        elif arg == '-u':
            if next is not None and next in ('admin', 'system', 'user', 'trusted'):
                default_config['user'] = user[next]
                i += 2
        else:
            i += 1

    return default_config


def get_log_time():
    """获取当前的时间"""
    return time.strftime("%Y年%m月%d日 %I时 %M分 %S秒", time.localtime())


def get_source_path():
    """获取真实的执行文件的路径"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        file_path = Path(sys.executable)
    else:
        if hasattr(__main__, "__file__"):
            file_path = Path(__main__.__file__)
        else:
            file_path = Path(__file__)
    return file_path


def error_log(file_name, comment=None):
    """打印错误log到文件信息"""
    log_name = path.dirname(get_source_path()) + fr"\{file_name}"
    with open(log_name, "a", encoding="utf8") as f:
        if comment:  # 如果有附带的说明那么就写入文件
            f.write(comment)
        f.write("\n" + get_log_time() + "\n")
        traceback.print_exc(file=f)


def info_log(file_name, comment=None):
    """打印信息到log文件"""
    log_name = path.dirname(get_source_path()) + fr"\{file_name}"
    with open(log_name, "a", encoding="utf8") as f:
        if comment:
            f.write("\n" + get_log_time() + "\n")
            f.write(comment)


def get_real_path(pstr):
    """得到LNK快捷文件和软链接的真实路径, 返回一个字符串"""
    final_path = None
    if pstr.endswith(".lnk"):
        # 如果是快捷方式那么就读取快捷方式的真实路径
        shell = Dispatch("WScript.Shell")
        final_path = shell.CreateShortCut(pstr).TargetPath
    elif path.islink(pstr):
        # 如果是软链接那么也获取真实的路径
        try:
            final_path = os.readlink(pstr)
        except Exception:
            return pstr
    else:
        final_path = pstr

    return final_path


def send_ctrl_c():
    """按下快捷键 ctrl + c"""
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(67, 0, 0, 0)
    time.sleep(0.1)
    win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)


def send_ctrl_shift_c():
    """按下快捷键 ctrl + shift + c"""
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(67, 0, 0, 0)
    win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)


def get_process_path(pid):
    """根据进程的pid获取进程的路径"""
    PROCESS_ALL_ACCESS = 0x1F0FFF
    processHandle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    modules = win32process.EnumProcessModules(processHandle)
    process_path = win32process.GetModuleFileNameEx(processHandle, modules[0])
    return process_path


def get_front_window_path():
    """获取激活窗口对应进程的路径"""
    hwnd = win32gui.GetForegroundWindow()
    # 获取进程id
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process_path = get_process_path(pid)
    return process_path


def get_all_process_path():
    """获取所有进程的路径"""
    pids = win32process.EnumProcesses()
    ps_path = []  # 存放进程路径的列表
    for pid in pids:
        try:
            p = get_process_path(pid)
        except Exception:
            continue
        else:
            ps_path.append(p)
    return ps_path


def is_frozen():
    """判断当前是否是单exe文件环境"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return True
    else:
        return False


__all__ = (
'get_log_time', 'get_source_path', 'error_log', 'get_real_path', 'send_ctrl_c', 'get_front_window_path', 'is_frozen',
'parse_argv', 'get_all_process_path')
