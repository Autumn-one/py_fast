import ctypes

MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_YESNO = 0x4
MB_ICONINFORMATION = 0x40
MB_ICONWARNING = 0x30
MB_ICONERROR = 0x10


def _show_message_box(message: str, title: str, type_: int, icon: int) -> int:
    """显示windows的消息框

    :param message: 消息内容
    :param title: 消息标题
    :param type_: 消息类型
    :param icon: 消息图标
    :return: 用户按钮的选择
    """
    return ctypes.windll.user32.MessageBoxW(None, message, title, type_ | icon)


def alert(message: str, title: str = "提示") -> None:
    """弹出一个普通的消息框

    :param message: 消息内容
    :param title: 消息标题
    """
    _show_message_box(message, title, MB_OK, MB_ICONINFORMATION)


def confirm(message: str, title: str = "确认") -> bool:
    """弹出一个确认框

    :param message: 消息内容
    :param title: 消息标题
    :return: True 表示确认，False 表示取消
    """
    return _show_message_box(message, title, MB_YESNO, MB_ICONWARNING) == 6


def prompt(title: str, message: str) -> str:
    """
    弹出一个对话框，用于获取用户输入的字符串

    :param title: 对话框的标题
    :param message: 对话框中的消息提示
    :return: 用户在对话框中输入的字符串
    """
    user32 = ctypes.windll.user32
    buf = ctypes.create_unicode_buffer(512)
    result = user32.GetWindowTextW(
        user32.GetForegroundWindow(),
        buf,
        512
    )
    buf = buf[:result]
    return buf

__all__ = [
    "alert",
    "confirm",
    "prompt"
]
