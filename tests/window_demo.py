import py_fast.windowx as wx

# wx.move_window2(0,0)

# print(wx.get_mouse_pos())

# wx.maximize_window()
# wx.minimize_window()
def mouse_fn(x,y):
    print("鼠标移动了")
    print(x,y)
wx.register_mousemove_callback(mouse_fn)