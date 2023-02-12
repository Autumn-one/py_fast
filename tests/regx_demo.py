# from py_fast.regx import get_list
import winreg
import py_fast.regx as wreg
import py_fast.message_box as message

# handle = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"Software\360Safe", 0, winreg.KEY_ALL_ACCESS)
# winreg.DeleteKey(handle,"ddd")
# print(type(handle) == winreg.HKEYType)
# print(str(handle))

# winreg.CreateKey(winreg.HKEY_CURRENT_USER, "哈哈哈aaa")
# winreg.CloseKey(handle)
# wreg.create(r"HKEY_CURRENT_USER\Network","haha丫丫")
# winreg.SetValue(winreg.HKEY_CURRENT_USER, "aabb", winreg.REG_SZ, "啦啦啦123")

# wreg.create(r"HKEY_LOCAL_MACHINE\SOFTWARE","",type="value_item",value="哈哈哈啦啦")

# winreg.SetValueEx(handle,"aaa",0,winreg.REG_SZ, "哈哈哈反而")

# wreg.set_value_item(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", "ccc压", "哈哈哈")

# wreg.get_list(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run")
# print(type(winreg.REG_BINARY))

# wreg.delete(r"HKEY_CURRENT_USER\Software\360Safe","aabb", safe=False)

from py_fast.message_box import *

# ret = show_question_box("请问你叫啥","一个问题")
# print(ret)

# message.alert("你好啊","标题")
# message.confirm("哈哈哈", "啦啦啦")

ret = message.prompt("请问你叫什么名字","输入名字")
print(ret)
