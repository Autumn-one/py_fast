"""
用于操作注册表的方法
"""
import winreg
from types import MappingProxyType
from typing import Tuple, Optional, Any, Union, Literal, TypeAlias, Type
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
    # 创建注册表项或值项或项的默认值，在创建项的默认值的时候不能给已经存在的项设置默认值，项和默认值的创建是一起的
    'create',
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
    root_key, child_key, _ = split_reg_str(key)
    if not root_key: return None

    key_list = []

    count = 0
    if child_key:
        with winreg.OpenKey(root_key, child_key, 0, winreg.KEY_ALL_ACCESS) as key:
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


def split_reg_str(reg_str: str) -> Tuple[Optional[int], Optional[str], Optional[str]]:
    """用于切割注册表字符串，返回三个值，一个是注册表的根常量，一个是剩余的注册表路径, 一个是路径中的最后一个项名称"""
    if reg_str.strip() == "": return None, None, None

    path_arr = reg_str.split('\\')
    root_key = path_arr[0]
    if root_key in root_key_map:
        # 说明有根键
        if len(path_arr) > 1:
            return root_key_map[root_key], reg_str[len(root_key) + 1:], path_arr[-1]
        else:
            return root_key_map[root_key], None, None

    else:
        # 没有根键
        return None, reg_str, path_arr[-1]


def get_parent(reg_path: str, return_type: Literal["str", "handle"] = "str") -> Union[HKEYType, str, int, None]:
    """传入一个注册表的键，这个可以是对象也可以是字符串，返回上一级的键
    如果传入是handle 那么久返回handle，如果传入的是字符串那么返回字符串，具体返回什么可以通过第二个参数指定
    """
    if reg_path.strip() == "": return None

    path_arr = reg_path.split("\\")
    if len(path_arr) == 1:
        if return_type == "str":
            return path_arr[0]
        else:
            return root_key_map[path_arr[0]]

    path_arr.pop()
    parent_path = "\\".join(path_arr)

    if return_type == "str":
        return parent_path
    else:
        return get_handle(parent_path)


def get_handle(key_path: Union[HKEYType, str]) -> Union[HKEYType, int, None]:
    """
    接受一个键的路径返回打开的 handle
    """
    if type(key_path) == HKEYType:
        return key_path
    root_key, sub_key, _ = split_reg_str(key_path)  # 获取根键和子键路径
    if root_key:
        if sub_key:
            return winreg.OpenKeyEx(root_key, sub_key, 0, winreg.KEY_ALL_ACCESS)
        else:
            return root_key
    else:
        return None


# 注册表的值类型，参照链接： https://docs.python.org/zh-cn/3/library/winreg.html?highlight=winreg#value-types
RegValueType: TypeAlias = Literal[
    # 任意格式的二进制数据。
    winreg.REG_BINARY,
        # 32 位数字。
    winreg.REG_DWORD,
        # 32 位低字节序格式的数字。相当于 REG_DWORD。
    winreg.REG_DWORD_LITTLE_ENDIAN,
        # 32 位高字节序格式的数字。
    winreg.REG_DWORD_BIG_ENDIAN,
        # 包含环境变量（%PATH%）的字符串，以空字符结尾。
    winreg.REG_EXPAND_SZ,
        # Unicode 符号链接。
    winreg.REG_LINK,
        # 一串以空字符结尾的字符串，最后以两个空字符结尾。Python 会自动处理这种结尾形式。
    winreg.REG_MULTI_SZ,
        # 未定义的类型。
    winreg.REG_NONE,
        # 64 位数字。
    winreg.REG_QWORD,
        # 64 位低字节序格式的数字。相当于 REG_QWORD。
    winreg.REG_QWORD_LITTLE_ENDIAN,
        # 设备驱动程序资源列表。
    winreg.REG_RESOURCE_LIST,
        # 硬件设置。
    winreg.REG_FULL_RESOURCE_DESCRIPTOR,
        # 硬件资源列表。
    winreg.REG_RESOURCE_REQUIREMENTS_LIST,
        # 空字符结尾的字符串。
    winreg.REG_SZ
]

# 注册表类型
RegType: TypeAlias = Union[HKEYType, str, int]


def create(base_key_path: RegType,
           key_name: Union[str, int],  # 要创建的键的名称，可能是项也可能是值项
           value: Optional[str] = None,
           *,
           type: Literal["item", "value_item"] = "item",
           value_type: RegValueType = winreg.REG_SZ) \
    -> None:
    """
    创建注册表的项或值,如果只是创建项那么直接写入
    base_key 在那个项的基础下创建
    key 创建的键的名称
    type 创建的是一个项还是一个值项
    value 如果是值项，那么这个值项的 value 是什么
    value_type 值项的值是多少
    """
    reg_handle = get_handle(base_key_path)
    if reg_handle is None: return

    if type == "item":
        winreg.CreateKeyEx(reg_handle, key_name)
    else:
        if key_name == "":
            winreg.SetValue(get_handle(get_parent(base_key_path)), key_name, value_type, value)
        else:
            winreg.SetValueEx(reg_handle, key_name, 0, value_type, value)

    winreg.CloseKey(reg_handle)


def create_item(base_path: RegType, item_name: str) -> None:
    """创建注册表项"""
    return create(base_path, item_name)


# 同 create_item 方法，创建一个注册表项
create_key = create_item


def create_value_item(base_path: RegType,
                      item_name: str,
                      value: Optional[str],
                      value_type: RegValueType = winreg.REG_SZ) -> None:
    # 专门创建注册表值的方法，无法用来创建项
    return create(base_path, item_name, value, value_type=value_type)


create_value = create_value_item


def set_value_item(base_path: Union[str, int], item_name: str, value: str,
                   value_type: RegValueType = winreg.REG_SZ) -> None:
    """设置值项的值，如果item_name 为空那么表示设置这个项的默认名称对应的值"""
    if item_name == "":
        reg_handle = get_parent(base_path, return_type="handle")
        _, _, last_item = split_reg_str(base_path)
        winreg.SetValue(reg_handle, last_item, winreg.REG_SZ,value)
    else:
        reg_handle = get_handle(base_path)
        winreg.SetValueEx(reg_handle, item_name, 0, value_type, value)
    winreg.CloseKey(reg_handle)
    return None

set_value = set_value_item

def delete(): ...  # 删除键


remove = delete


def delete_item(): ...


def delete_value(): ...


def raname(): ...  # 修改注册表项或值的名称




def export_file(): ...  # 导出为注册表文件


def load_file(): ...  # 加载注册表文件
