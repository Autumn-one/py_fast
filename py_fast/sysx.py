# 系统相关功能, 包含进程的获取等
import ctypes
import os, win32api, win32gui, win32process
import os
import win32com.client
from typing import Optional, Union
from pathlib import Path

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

def create_shortcut(path: Union[Path, str], name: str, shortcut_path: Optional[Union[Path, str]] = None) -> None:
    """
    创建一个快捷方式到指定路径。
    :param path: 快捷方式指向的目标路径（Path对象或字符串）。
    :param name: 快捷方式的名称。
    :param shortcut_path: 快捷方式的保存路径（Path对象或字符串）。如果未提供，则使用目标路径所在的文件夹。
    """
    # 确保path是Path对象
    if not isinstance(path, Path):
        path = Path(path)

    # 处理shortcut_path
    if shortcut_path is None:
        shortcut_path = path.parent
    elif not isinstance(shortcut_path, Path):
        shortcut_path = Path(shortcut_path)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path.joinpath(name + '.lnk')))
    shortcut.Targetpath = str(path)
    shortcut.WorkingDirectory = str(path.parent)
    shortcut.save()

