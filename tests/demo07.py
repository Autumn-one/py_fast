import subprocess
import sys

def install_and_restart(module_name):
    """
    安装指定的Python模块，并重启脚本。

    :param module_name: 模块名称
    """
    # 使用pip命令安装模块
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
    # 重新运行当前脚本
    subprocess.check_call([sys.executable] + sys.argv)

# 尝试导入需要的模块，这里以requests为例
try:
    import requests
except ImportError:
    # 如果导入失败，安装模块并重启脚本
    install_and_restart("requests")
else:
    # 模块导入成功，继续执行脚本的其他部分
    print("模块已存在，继续执行脚本。")