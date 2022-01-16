from os import path
import os

is_abs = path.isabs
is_file = path.isfile
is_dir = path.isdir
is_link = is_symlink = path.islink # 重命名判断软链接的方法
cwd = os.getcwd # 获取当前工作目录


