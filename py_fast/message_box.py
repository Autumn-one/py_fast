import ctypes

MessageBox = ctypes.windll.user32.MessageBoxW

__all__ = (
    "show_message_box",
    "show_info_box",
    "show_warning_box",
    "show_error_box",
    "show_question_box"
)


def show_message_box(text: str, title: str = "消息", type: int = 0x40):
    """
    显示消息对话框
    text 表示对话框中显示的文本
    title 表示对话框标题
    type 表示对话框的类型
    """
    return MessageBox(None, text, title, type)


def show_info_box(text: str, title: str = "消息"):
    """
    显示信息对话框
    text 表示对话框中显示的文本
    title 表示对话框标题
    """
    return show_message_box(text, title, 0x40)


def show_warning_box(text: str, title: str = "警告"):
    """
    显示警告对话框
    text 表示对话框中显示的文本
    title 表示对话框标题
    """
    return show_message_box(text, title, 0x30)


def show_error_box(text: str, title: str = "错误"):
    """
    显示错误对话框
    text 表示对话框中显示的文本
    title 表示对话框标题
    """
    return show_message_box(text, title, 0x10)


def show_question_box(text: str, title: str = "询问"):
    """
    显示询问对话框
    text 表示对话框中显示的文本
    title 表示对话框标题
    """
    return show_message_box(text, title, 0x20)
