import win32con

import py_fast.windowx as wx

# wx.move_window2(0,0)

# print(wx.get_mouse_pos())

# wx.maximize_window()
# wx.minimize_window()


# 导入mouse模块，它可以监听和控制鼠标事件
import mouse


# 定义一个回调函数，它接受一个鼠标事件对象作为参数
# 鼠标事件对象包含有event_type, x, y等属性
# 使用类型注解来指定参数和返回值的类型[^4^][4] [^5^][5] [^6^][6]
def mouse_move_callback(event: mouse.MoveEvent) -> None:
    # 打印鼠标的坐标信息
    print(event)



# 注册回调函数到mouse模块中，让它在每次鼠标移动时被调用
mouse.hook(mouse_move_callback)

# 等待用户按下Ctrl+C来退出程序
print("Press Ctrl+C to exit")
mouse.wait()



# 导入keyboard库
import keyboard

# 定义一个函数，用于处理按键事件
def on_press(event: keyboard.KeyboardEvent) -> None:
    # 获取按键名称和扫描码
    name = event.name
    scan_code = event.scan_code
    # 打印按键信息
    print(f"You pressed {name} with scan code {scan_code}")

# 注册一个全局的热键钩子，当任意按键被按下时调用on_press函数
keyboard.on_press(on_press)
# 开始监听键盘事件，直到用户终止程序或者触发异常
keyboard.wait()

