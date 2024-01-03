"""pywin32 的封装"""

import __main__
import ctypes
import os
import sys
import threading
import time
import tkinter as tk
import traceback
from os import path
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any

import keyboard
import mouse
import win32con
import win32gui
import win32process
from win32com.client import Dispatch

__all__ = (
    'get_log_time', 'get_source_path', 'error_log', 'get_real_path', 'send_ctrl_c', 'get_front_window_path',
    'is_frozen',
    'parse_argv', 'get_all_process_path', 'get_window_titles_and_processes', 'move_window')


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


def get_front_window():
    """获取最前面的窗口句柄"""
    return win32gui.GetForegroundWindow()


def set_front_window(hwnd):
    """设置指定的句柄为最前面的窗口"""
    return win32gui.SetForegroundWindow(hwnd)


def get_window_title(hwnd):
    """获取传入窗口句柄的标题"""
    return win32gui.GetWindowText(hwnd)


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


def find_window_by_title(title):
    """通过标题获取窗口的句柄"""
    try:
        return win32gui.FindWindow(None, title)
    except Exception as ex:
        print('error calling win32gui.FindWindow ' + str(ex))
        return -1


def get_window_titles_and_processes() -> List[Dict[str, str]]:
    """
    获取所有窗口标题和进程路径

    返回值：
    [
        {
            "title": 窗口标题,
            "process": 进程路径
        },
        ...
    ]
    """
    window_titles_and_processes: List[Dict[str, str]] = []

    # 获取所有窗口的句柄
    def callback(hwnd: int, _) -> bool:
        # 如果窗口可见，则获取窗口标题和进程路径
        if win32gui.IsWindowVisible(hwnd):
            title: str = win32gui.GetWindowText(hwnd)
            pid: int = win32process.GetWindowThreadProcessId(hwnd)[1]
            process_path: str = win32process.GetModuleFileNameEx(win32api.OpenProcess(0x0400, False, pid), 0)
            window_titles_and_processes.append({"title": title, "process": process_path})
        return True

    win32gui.EnumWindows(callback, None)

    return window_titles_and_processes


def move_window(
        x: int = 0,
        y: int = 0,
        hwnd: Optional[int] = None,
) -> bool:
    """
    移动窗口

    参数：
    - hwnd: 窗口句柄，默认为 None，表示当前激活的窗口
    - x: 要移动到的 x 坐标，默认为 0
    - y: 要移动到的 y 坐标，默认为 0

    返回值：
    - 如果窗口移动成功，返回 True；否则返回 False
    """
    # 如果未传入 hwnd，使用 GetForegroundWindow 函数获取当前激活的窗口句柄
    if hwnd is None:
        hwnd = win32gui.GetForegroundWindow()

    # 获取窗口当前位置和大小
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # 计算窗口要移动到的位置
    new_left = x
    new_top = y
    new_right = new_left + width
    new_bottom = new_top + height

    # 移动窗口
    result = win32gui.MoveWindow(hwnd, new_left, new_top, width, height, True)

    return result

import win32api
from typing import Tuple


def get_mouse_pos() -> Tuple[int, int]:
    """
    获取当前鼠标位置
    :return: (x, y) 坐标元组
    """
    x, y = win32api.GetCursorPos()
    return x, y

def get_window_border_width(hwnd: int) -> tuple[int, int, int, int]:
    """
    获取窗口的边框宽度（左边框、上边框、右边框、下边框）
    """
    style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
    ex_style = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    border_width_left = (rect[2] - rect[0] - client_rect[2]) // 2
    border_width_top = (rect[3] - rect[1] - client_rect[3]) - border_width_left
    border_width_right = border_width_left + (rect[2] - rect[0] - client_rect[2]) % 2
    border_width_bottom = border_width_top + (rect[3] - rect[1] - client_rect[3]) % 2
    return border_width_left, border_width_top, border_width_right, border_width_bottom


def maximize_window(hwnd: Optional[int] = None) -> None:
    """
    最大化指定窗口，如果未指定窗口句柄则最大化当前激活窗口。

    Args:
        hwnd: 可选，指定要最大化的窗口句柄。

    Returns:
        None

    """
    if hwnd is None:
        hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

def minimize_window(hwnd: Optional[int] = None) -> None:
    """
    最小化指定窗口，如果未指定窗口句柄则最小化当前激活窗口。

    Args:
        hwnd: 可选，指定要最小化的窗口句柄。

    Returns:
        None

    """
    if hwnd is None:
        hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def register_keyboard_events(on_press: Callable[[Any], None]) -> None:
    """注册系统的键盘钩子"""
    # def on_press(event: keyboard.KeyboardEvent) -> None:
    #     # 获取按键名称和扫描码
    #     name = event.name
    #     scan_code = event.scan_code
    #     # 打印按键信息
    #     print(f"You pressed {name} with scan code {scan_code}")

    # 注册一个全局的热键钩子，当任意按键被按下时调用on_press函数
    keyboard.on_press(on_press)
    # 开始监听键盘事件，直到用户终止程序或者触发异常
    keyboard.wait()


def register_mouse_move_events(mouse_move_callback: Callable[[Any], None]):
    """
    注册系统的鼠标移动回调
    """
    # def mouse_move_callback(event: mouse.MoveEvent) -> None:
    #     # 打印鼠标的坐标信息
    #     print(event)

    # 注册回调函数到mouse模块中，让它在每次鼠标移动时被调用
    mouse.hook(mouse_move_callback)

    # 等待用户按下Ctrl+C来退出程序
    print("Press Ctrl+C to exit")
    mouse.wait()


def get_input_chinese_and_english_status():
    """
    得到输入法的中英文的状态
    """
    imm32 = ctypes.windll.imm32
    user32 = ctypes.windll.user32

    # 获取 ImmGetDefaultIMEWnd 函数
    ImmGetDefaultIMEWnd = imm32.ImmGetDefaultIMEWnd

    # 调用 ImmGetDefaultIMEWnd 函数，并传入参数 None
    h = win32gui.GetForegroundWindow()
    im_window = ImmGetDefaultIMEWnd(h)

    ret = user32.SendMessageA(im_window, 0x0283, 0x0005, 0)
    return "中" if ret == 1 else "英"



def is_admin() -> bool:
    """
    检查当前进程是否以管理员权限运行。

    :return: 如果程序以管理员权限运行则返回True，否则返回False。
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(executable_path: Optional[str] = None, argv: Optional[list[str]] = None, debug: bool = False) -> Optional[bool]:
    """
    以管理员权限运行指定的程序或重新以管理员权限启动当前程序。

    :param executable_path: 要以管理员权限运行的程序的路径。如果为None，则重启当前程序。
    :param argv: 命令行参数列表。默认为None，此时使用sys.argv。
    :param debug: 是否打印调试信息。默认为False。
    :return: 如果程序已是管理员权限或重启成功则返回True，用户拒绝提升权限返回False，程序重启中返回None。
    """
    shell32 = ctypes.windll.shell32

    if argv is None:
        argv = sys.argv
    if executable_path is None:
        executable_path = sys.executable

    if hasattr(sys, '_MEIPASS'):
        # 支持PyInstaller打包后的可执行文件
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)

    argument_line = u' '.join(arguments)
    if debug:
        print('命令行:', executable_path, argument_line)

    ret = shell32.ShellExecuteW(None, "runas", executable_path, argument_line, None, 1)
    if ret <= 32:
        return False
    return None


def is_current_window_maximized() -> bool:
    """
    检测当前窗口是否是最大化。

    :return: 如果当前窗口是最大化返回True，否则返回False。
    """
    # 获取当前处于前台的窗口句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口的放置状态
    placement = win32gui.GetWindowPlacement(hwnd)

    # 检查窗口是否处于最大化状态
    return placement[1] == win32con.SW_SHOWMAXIMIZED



def is_current_window_minimized() -> bool:
    """
    检测当前窗口是否是最小化。

    :return: 如果当前窗口是最小化返回True，否则返回False。
    """
    # 获取当前处于前台的窗口句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口的放置状态
    placement = win32gui.GetWindowPlacement(hwnd)

    # 检查窗口是否处于最小化状态
    return placement[1] == win32con.SW_SHOWMINIMIZED


def show_floating_message(message: str, duration: int = 3000, offset: tuple = None):
    """
    在屏幕上显示一个浮动的消息提示。

    :param message: 要显示的文本。
    :param duration: 消息显示的持续时间（毫秒），默认为3000毫秒。
    :param offset: 消息框的偏移量，格式为(x, y)。如果为None，则显示在屏幕中间。
    """
    def message_window():
        popup = tk.Tk()
        popup.overrideredirect(True)  # 无边框窗口
        popup.attributes("-topmost", True)  # 窗口置顶
        popup.geometry(f"+{offset_x}+{offset_y}")  # 设置位置
        label = tk.Label(popup, text=message, bg="black", fg="white", padx=10, pady=5)
        label.pack()
        popup.after(duration, popup.destroy)  # 设置持续时间后自动销毁
        popup.mainloop()

    # 创建一个临时窗口以获取屏幕尺寸
    temp_window = tk.Tk()
    screen_width = temp_window.winfo_screenwidth()
    screen_height = temp_window.winfo_screenheight()
    temp_window.destroy()

    # 计算消息窗口的位置
    offset_x = (screen_width // 2) if offset is None else offset[0]
    offset_y = (screen_height // 2) if offset is None else offset[1]

    # 创建并启动线程
    threading.Thread(target=message_window, daemon=True).start()