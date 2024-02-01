import ctypes
from tkinter import *
from typing import Tuple

import win32api
import win32gui


def is_ctrl_pressed():
    # 获取 Ctrl 键的状态
    ctrl_state = win32api.GetKeyState(0x11)
    # 如果 Ctrl 键被按下，则最高位为 1
    return ctrl_state & (1 << 7) != 0



def get_mouse_pos() -> Tuple[int, int]:
    """
    获取当前鼠标位置
    :return: (x, y) 坐标元组
    """
    x, y = win32api.GetCursorPos()
    return x, y


def get_input_chinese_and_english_status():
    """
    得到输入法的中英文的状态
    """
    imm32 = ctypes.windll.imm32
    user32 = ctypes.windll.user32

    # 获取 ImmGetDefaultIMEWnd 函数
    ImmGetDefaultIMEWnd = imm32.ImmGetDefaultIMEWnd

    # 调用 ImmGetDefaultIMEWnd 函数，并传入参数 None
    h = win32gui.GetForegroundWindow()
    im_window = ImmGetDefaultIMEWnd(h)

    ret = user32.SendMessageA(im_window, 0x0283, 0x0005, 0)
    return "中" if ret == 1 else "英"

root = Tk() # 创建主窗口
root.overrideredirect(True)
root.attributes("-topmost",1)
root.attributes("-alpha",0.5)
root.geometry("40x40")
img_chinese = PhotoImage(file="./中.png")
img_english = PhotoImage(file="./英.png")

# 定义偏移量
offset_x = 50
offset_y = -30
label = Label(root, borderwidth=0, width=40, height=40) # 创建标签
label.place(x=0, y=0) # 显示标签，并设置位置
def move_window():

    if is_ctrl_pressed():
        root.withdraw()
    else:
        root.update()
        root.deiconify()

    try:
        x,y = get_mouse_pos()
    except:
        root.withdraw()
        x = 0
        y=0

    x += offset_x
    y += offset_y
    root.geometry(f'+{x}+{y}')
    input_status = get_input_chinese_and_english_status()
    if input_status == "中":
        label.configure(image=img_chinese)
    else:
        label.configure(image=img_english)
    # 使用 after() 方法进行递归调用，以实现持续触发该函数
    root.after(2, lambda: move_window())

root.after(2,lambda: move_window())


root.mainloop() # 进入主循环