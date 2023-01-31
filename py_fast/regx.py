"""
用于操作注册表的方法
"""
import winreg
from types import MappingProxyType
from typing import Tuple, Optional, Any, Union, Literal, TypeAlias
from winreg import HKEYType

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
    "HKEY_CLASSES_ROOT"    : HKEY_CLASSES_ROOT,
    "HKCR"                 : HKCR,

    "HKEY_CURRENT_USER"    : HKEY_CURRENT_USER,
    "HKCU"                 : HKCU,

    "HKEY_CURRENT_CONFIG"  : HKEY_CURRENT_CONFIG,
    "HKCC"                 : HKCC,

    "HKEY_LOCAL_MACHINE"   : HKEY_LOCAL_MACHINE,
    "HKLM"                 : HKLM,

    "HKEY_USERS"           : HKEY_USERS,
    "HKU"                  : HKU,

    "HKEY_DYN_DATA"        : HKEY_DYN_DATA,
    "HKDD"                 : HKDD,

    "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
    "HKPD"                 : HKPD
})


def get_list(key=None):
    """
    获得对应key下面的所有项和值，返回一个列表，列表项形如：
    {
        type: "item",
        key: "abc"
        value: None
    }
    或
    {
        type: "value_item",
        key: "ccc",
        value: "abc",
        value_type: winreg.REG_BINARY
    }
    """
    root_key, child_key = split_reg_str(key)
    if not root_key: return None

    key_list = []

    count = 0
    if child_key:
        with winreg.OpenKey(root_key, child_key) as key:
            try:
                while True:
                    k = winreg.EnumKey(key, count)
                    key_list.append({
                        'type' : 'item',
                        'key'  : k,
                        'value': None
                    })
                    count += 1
            except OSError:
                ...
            finally:
                count = 0

            try:
                while True:
                    key_name, value, value_type = winreg.EnumValue(key, count)
                    key_list.append({
                        'type'      : 'value_item',
                        'key'       : key_name,
                        'value'     : value,
                        'value_type': value_type
                    })
                    count += 1
            except OSError:
                ...
            finally:
                del count

        return key_list
    else:
        # 遍历所有的注册表项
        try:
            while True:
                k = winreg.EnumKey(root_key, count)
                key_list.append({
                    'type' : 'item',
                    'key'  : k,
                    'value': None
                })
                count += 1
        except OSError:
            ...
        finally:
            count = 0
        # 遍历所有的注册表值
        try:
            while True:
                key_name, value, value_type = winreg.EnumValue(root_key, count)
                key_list.append({
                    'type'      : 'value_item',
                    'key'       : key_name,
                    'value'     : value,
                    'value_type': value_type
                })
                count += 1
        except OSError:
            ...
        finally:
            del count

        return key_list


def transform_root_key(key: str) -> Optional[int]:
    """根据传入的str转换为根键并返回，如果无法返回根键那么直接返回 None"""
    if key.strip() == "": return None

    if key in root_key_map:
        return root_key_map[key]
    else:
        return None


def split_reg_str(reg_str: str) -> Tuple[Optional[int], Optional[str]]:
    """用于切割注册表字符串，返回两个值，一个是注册表的根常量，一个是剩余的注册表路径"""
    if reg_str.strip() == "": return None, None

    path_arr = reg_str.split('\\')
    root_key = path_arr[0]
    if root_key in root_key_map:
        # 说明有根键
        if len(path_arr) > 1:
            return root_key_map[root_key], reg_str[len(root_key) + 1:]
        else:
            return root_key_map[root_key], None

    else:
        # 没有根键
        return None, reg_str


def get_handle(key_path: str) -> Optional[HKEYType | int]:
    """
    接受一个键的路径返回打开的 handle
    """
    root_key, sub_key = split_reg_str(key_path)  # 获取根键和子键路径
    if root_key:
        if sub_key:
            return winreg.OpenKeyEx(root_key, sub_key)
        else:
            return root_key
    else:
        return None

# 注册表的值类型，参照链接： https://docs.python.org/zh-cn/3/library/winreg.html?highlight=winreg#value-types
REG_VALUE_TYPE: TypeAlias = \
    winreg.REG_BINARY \
    | winreg.REG_DWORD \
    | winreg.REG_DWORD_LITTLE_ENDIAN \
    | winreg.REG_DWORD_BIG_ENDIAN \
    | winreg.REG_EXPAND_SZ \
    | winreg.REG_LINK \
    | winreg.REG_MULTI_SZ \
    | winreg.REG_NONE \
    | winreg.REG_QWORD \
    | winreg.REG_QWORD_LITTLE_ENDIAN \
    | winreg.REG_RESOURCE_LIST \
    | winreg.REG_FULL_RESOURCE_DESCRIPTOR \
    | winreg.REG_RESOURCE_REQUIREMENTS_LIST \
    | winreg.REG_SZ
def create(base_key: Union[HKEYType, str, int],
           key: Union[str, int],
           value: Optional[str] = None,
           *,
           type: Literal["item", "value_item"] = "item",
           value_type: REG_VALUE_TYPE = winreg.REG_SZ) \
    -> None:
    """
    创建注册表的项或值,如果只是创建项那么直接写入
    base_key 在那个项的基础下创建
    key 创建的键的名称
    type 创建的是一个项还是一个值项
    value 如果是值项，那么这个值项的 value 是什么
    value_type 值项的值是多少
    """
    reg_handle = get_handle(base_key)
    if reg_handle is None: return

    if type == "item":
        winreg.CreateKeyEx(reg_handle, key)
    else:
        winreg.SetValueEx(reg_handle, key, 0, value_type, value)

    winreg.CloseKey(reg_handle)


create_key = create


def create_item(): ...  # 创建注册表的项


def create_value(): ...  # 专门创建注册表值的方法，无法用来创建项


def delete(): ...  # 删除键


remove = delete


def delete_item(): ...


def delete_value(): ...


def raname(): ...  # 修改注册表项或值的名称


def set_value(): ...  # 设置注册表值的信息


def export_file(): ...  # 导出为注册表文件


def load_file(): ...  # 加载注册表文件
