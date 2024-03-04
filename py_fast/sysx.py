# 系统相关功能, 包含进程的获取等
import ctypes
import os, win32api, win32gui, win32process
import os
import win32com.client
from typing import Optional, Union
from pathlib import Path
import string
import random

__all__ = (
    "get_env",
    "get_process_path",
    "get_front_window_path",
    "get_all_process_path",
    "get_front_window_process",
    "get_process_threads"
)

from ctypes import wintypes

from typing import Optional, List, Tuple, Dict

import win32con


def get_env(env_str: str):
    """
    获取系统的环境变量, 传入一个环境变量的字符串返回环境变量的值
    传入的值可以带%可以不带%
    """
    if env_str.startswith("%"):
        env_str = env_str.strip("%")

    return os.environ.get(env_str,None)


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

def get_front_window_process():
    """获取激活窗口对应的进程"""
    hwnd = win32gui.GetForegroundWindow()
    # 获取进程id
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def get_all_process_path():
    """获取所有进程的路径"""
    pids = win32process.EnumProcesses()
    ps_path = [] # 存放进程路径的列表
    for pid in pids:
        try:
            p = get_process_path(pid)
        except Exception:
            continue
        else:
            ps_path.append(p)
    return ps_path

# 定义THREADENTRY32结构
class THREADENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ThreadID", wintypes.DWORD),
                ("th32OwnerProcessID", wintypes.DWORD),
                ("tpBasePri", wintypes.LONG),
                ("tpDeltaPri", wintypes.LONG),
                ("dwFlags", wintypes.DWORD)]

# 定义TH32CS_SNAPTHREAD
TH32CS_SNAPTHREAD = 0x00000004
INVALID_HANDLE_VALUE = -1

def get_process_threads(pid: int) -> Optional[List[Tuple[int, int]]]:
    """
    获取指定进程的线程列表。

    :param pid: 进程ID。
    :return: 一个包含线程ID和基础优先级的列表，如果进程不存在则返回None。
    """
    hSnapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if hSnapshot == INVALID_HANDLE_VALUE:
        return None

    thread_entry = THREADENTRY32()
    thread_entry.dwSize = ctypes.sizeof(THREADENTRY32)
    thread_list = []

    if ctypes.windll.kernel32.Thread32First(hSnapshot, ctypes.byref(thread_entry)):
        while True:
            if thread_entry.th32OwnerProcessID == pid:
                thread_list.append((thread_entry.th32ThreadID, thread_entry.tpBasePri))

            if not ctypes.windll.kernel32.Thread32Next(hSnapshot, ctypes.byref(thread_entry)):
                break

    ctypes.windll.kernel32.CloseHandle(hSnapshot)
    return thread_list


def get_thread_info(thread_id: int) -> Optional[Dict]:
    """
    获取指定线程的详细信息。

    :param thread_id: 线程ID。
    :return: 包含线程信息的字典，如果线程不存在则返回None。
    """
    ...
    # thread_info = {}
    # try:
    #     # 打开线程句柄
    #     h_thread = win32api.OpenThread(win32con.THREAD_QUERY_INFORMATION, False, thread_id)
    #
    #     # 获取线程的优先级
    #     priority = win32process.GetThreadPriority(h_thread)
    #     thread_info['priority'] = priority
    #
    #     # 使用ctypes调用NtQueryInformationThread获取线程所属进程ID
    #     process_id = ctypes.c_ulong()
    #     ctypes.windll.ntdll.NtQueryInformationThread(h_thread, 9, ctypes.byref(process_id), ctypes.sizeof(process_id), None)
    #     thread_info['process_id'] = process_id.value
    #
    #     # 关闭线程句柄
    #     win32api.CloseHandle(h_thread)
    #
    #     return thread_info
    # except Exception as e:
    #     # 如果发生错误，例如线程不存在
    #     return None

import os
import win32com.client
from typing import Optional, Union
from pathlib import Path

def create_shortcut(*args: Union[Path, str]) -> None:
    """
    创建一个快捷方式到指定路径。可以接收两个或三个参数。
    - 如果传入两个参数，第一个是源文件/文件夹的路径，第二个是目标文件/文件夹的路径。
    - 如果传入三个参数，第一个是源文件/文件夹的路径，第二个是快捷方式的名称，第三个是快捷方式的保存路径。
    :param args: 可变参数，可以是Path对象或字符串。
    """
    if len(args) == 2:
        path, shortcut_path = args
        name = os.path.basename(path)
    elif len(args) == 3:
        path, name, shortcut_path = args
    else:
        raise ValueError("Invalid number of arguments. Expected 2 or 3 arguments.")

    # 确保path和shortcut_path是Path对象
    path = Path(path) if not isinstance(path, Path) else path
    shortcut_path = Path(shortcut_path) if not isinstance(shortcut_path, Path) else shortcut_path

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path.joinpath(name + '.lnk')))
    shortcut.Targetpath = str(path)
    shortcut.WorkingDirectory = str(path.parent)
    shortcut.save()


import os
from pathlib import Path
from typing import Union

def create_hard_link(source: Union[Path, str], link_name: Union[Path, str]) -> None:
    """
    创建一个指向文件的硬链接。
    :param source: 源文件的路径（可以是Path对象或字符串）。
    :param link_name: 硬链接的路径（可以是Path对象或字符串）。
    """
    source = Path(source) if not isinstance(source, Path) else source
    link_name = Path(link_name) if not isinstance(link_name, Path) else link_name

    os.link(source, link_name)

def generate_password(length=8):
    # 所有可能的字符包括大写、小写字母和数字
    all_characters = string.ascii_letters + string.digits

    # 如果你还需要添加标点符号，可以在上面的行里加入 string.punctuation

    # 使用 random.choice 随机选择字符，组成密码
    password = ''.join(random.choice(all_characters) for _ in range(length))

    return password