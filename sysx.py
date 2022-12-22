# 系统相关功能, 包含进程的获取等
import os, win32api, win32gui, win32process

__all__ = (
    "get_env",
    "get_process_path",
    "get_front_window_path",
    "get_all_process_path"
)

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


