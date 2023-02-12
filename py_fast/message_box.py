# 封装了系统弹窗的页面

import ctypes
from ctypes import wintypes

# 加载 WebView2 运行时
ctypes.WinDLL("WebView2Loader.dll")

# 加载 WebView2 API
webView2Api = ctypes.WinDLL("WebView2Api.dll")

# 定义回调函数
def on_navigation_starting(webView, args, cancelling):
    url = args.get_uri()
    print("正在导航到", url)

# 创建 CoreWebView2Environment
webView2Environment = ctypes.c_void_p()
result = webView2Api.CreateCoreWebView2EnvironmentWithDetails(
    None,
    None,
    None,
    ctypes.byref(webView2Environment)
)

# 创建 CoreWebView2
webView2 = ctypes.c_void_p()
result = webView2Api.CreateCoreWebView2(
    webView2Environment,
    None,
    ctypes.byref(webView2)
)

# 设置回调函数
on_navigation_starting_callback_type = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_void_p
)
on_navigation_starting_callback = on_navigation_starting_callback_type(
    on_navigation_starting
)

result = webView2Api.AddCoreWebView2NavigationStartingEvent(
    webView2,
    on_navigation_starting_callback,
    None
)

# 导航到 URL
result = webView2Api.Navigate(webView2, "https://www.microsoft.com")

# 等待用户输入以关闭应用程序
input()

# 清理
result = webView2Api.CloseCoreWebView2(webView2)
result = webView2Api.DestroyCoreWebView2Environment(webView2Environment)
