# from py_fast.regx import get_list
import winreg
import py_fast.regx as wreg

# handle = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"Software", 0, winreg.KEY_ALL_ACCESS)

# print(str(handle))

# winreg.CreateKey(winreg.HKEY_CURRENT_USER, "哈哈哈aaa")
# winreg.CloseKey(handle)
# wreg.create(r"HKEY_CURRENT_USER\Network","haha丫丫")
# winreg.SetValue(winreg.HKEY_CURRENT_USER, "aabb", winreg.REG_SZ, "啦啦啦123")

# wreg.create(r"HKEY_LOCAL_MACHINE\SOFTWARE","",type="value_item",value="哈哈哈啦啦")

# winreg.SetValueEx(handle,"aaa",0,winreg.REG_SZ, "哈哈哈反而")

wreg.set_value_item(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", "ccc压", "哈哈哈")
