# 系统相关功能
import os

def get_env(env_str: str):
    """
    获取系统的环境变量, 传入一个环境变量的字符串返回环境变量的值
    传入的值可以带%可以不带%
    """
    if env_str.startswith("%"):
        env_str = env_str.strip("%")

    return os.environ.get(env_str,None)

