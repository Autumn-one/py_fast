from py_fast.regx import get_list
import winreg
import py_fast.regx as wreg

# handle = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER)

# winreg.CreateKey(winreg.HKEY_CURRENT_USER, "哈哈哈aaa")
# winreg.CloseKey(handle)
# wreg.create(r"HKEY_CURRENT_USER\Network","haha丫丫")
winreg.SetValueEx(winreg.HKEY_CURRENT_USER, "aabb", 0, winreg.REG_SZ, "啦啦啦")
