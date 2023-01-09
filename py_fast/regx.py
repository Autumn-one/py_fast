"""
用于操作注册表的方法
"""
from typing import Tuple, Union, Optional
from types import MappingProxyType
import winreg

__all__ = (
    # 注册表根键导出
    'HKEY_CLASSES_ROOT', 'HKCR',
    'HKEY_CURRENT_USER', 'HKCU',
    'HKEY_CURRENT_CONFIG', 'HKCC',
    'HKEY_LOCAL_MACHINE', 'HKLM',
    'HKEY_USERS', 'HKU',
    'HKEY_DYN_DATA', 'HKDD',
    'HKEY_PERFORMANCE_DATA', 'HKPD',

    # 获取注册表的列表
    'get_list',
)

# 本注册表键下的注册表项定义了文件的类型（或类别）及相关属性。Shell 和 COM 应用程序将使用该注册表键下保存的信息。
HKEY_CLASSES_ROOT = HKCR = winreg.HKEY_CLASSES_ROOT

# 属于该注册表键的表项定义了当前用户的偏好。这些偏好值包括环境变量设置、程序组数据、颜色、打印机、网络连接和应用程序参数。
HKEY_CURRENT_USER = HKCU = winreg.HKEY_CURRENT_USER

# 包含有关本地计算机系统当前硬件配置的信息。
HKEY_CURRENT_CONFIG = HKCC = winreg.HKEY_CURRENT_CONFIG

# 属于该注册表键的表项定义了计算机的物理状态，包括总线类型、系统内存和已安装软硬件等数据。
HKEY_LOCAL_MACHINE = HKLM = winreg.HKEY_LOCAL_MACHINE

# 属于该注册表键的表项定义了当前计算机中新用户的默认配置和当前用户配置。
HKEY_USERS = HKU = winreg.HKEY_USERS

# Windows 98 以上版本不使用该注册表键。
HKEY_DYN_DATA = HKDD = winreg.HKEY_DYN_DATA

# 属于该注册表键的表项可用于读取性能数据。这些数据其实并不存放于注册表中；注册表提供功能让系统收集数据。
HKEY_PERFORMANCE_DATA = HKPD = winreg.HKEY_PERFORMANCE_DATA


# 注册表所有的根键映射, 这是一个只读的map
root_key_map = MappingProxyType({
    "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
    "HKCR": HKCR,

    "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
    "HKCU": HKCU,

    "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG,
    "HKCC": HKCC,

    "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
    "HKLM": HKLM,

    "HKEY_USERS": HKEY_USERS,
    "HKU": HKU,

    "HKEY_DYN_DATA": HKEY_DYN_DATA,
    "HKDD": HKDD,

    "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
    "HKPD": HKPD
})

def get_list(key = None):
    """
    获得对应key下面的value
    """
    ...


def transform_root_key(key: str) -> Optional[int]:
    """根据传入的str转换根键"""
    if key.strip() == "": return None

    if key in root_key_map:
        return root_key_map[key]
    else:
        return None

def split_reg_str(reg_str: str) -> Tuple[Optional[int],Optional[str]]:
    """用于切割注册表字符串，返回两个值，一个是注册表的根常量，一个是剩余的注册表路径"""
    if reg_str.strip() == "": return None, None

    path_arr = reg_str.split('\\')
    root_key = path_arr[0]
    if root_key in root_key_map:
        # 说明有根键
        if len(path_arr) > 1:
            return root_key_map[root_key], reg_str[len(root_key)+1:]
        else:
            return root_key_map[root_key], None

    else:
        # 没有根键
        return None, reg_str