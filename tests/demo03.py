import win32gui
import win32api
import win32con

# 获取当前活动窗口的句柄
hwnd = win32gui.GetForegroundWindow()

# 获取编辑框控件的句柄
edit_hwnd = win32gui.FindWindowEx(hwnd, None, "Edit", None)

# 获取插入点的位置
index = win32api.SendMessage(edit_hwnd, win32con.EM_GETSEL, 0, 0)[0]

# 获取插入点所在行的位置
line_index = win32api.SendMessage(edit_hwnd, win32con.EM_LINEINDEX, -1, 0)

# 获取插入点所在行的文本
line_text = win32gui.SendMessage(edit_hwnd, win32con.EM_GETLINE, line_index, 0)

# 计算插入点相对于屏幕的坐标位置
x, y = win32gui.SendMessage(edit_hwnd, win32con.EM_POSFROMCHAR, index, 0)

# 获取编辑框控件相对于屏幕的坐标位置
edit_rect = win32gui.GetWindowRect(edit_hwnd)
edit_x, edit_y = edit_rect[:2]

# 计算插入点相对于屏幕的坐标位置
screen_x, screen_y = edit_x + x, edit_y + y

print(f"插入点相对于屏幕的坐标位置为 ({screen_x}, {screen_y})")
