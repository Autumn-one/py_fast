import argparse
import shlex

# try:
#     abc = 1
# finally:
#     ccc = 2
#
# print(abc)
# 命令行字符串
command_string = "cfg -cmd -window max"

# 使用shlex.split分割命令字符串
args_list = shlex.split(command_string)

# 创建解析器
parser = argparse.ArgumentParser(description='命令行参数解析示例')

# 添加参数
parser.add_argument('-cmd', help='是否是一条命令', action="store_true")
parser.add_argument('-user', help='用那个权限', type=str, choices=["a", "n", "s", "t"], default="a")
parser.add_argument('-window', help='窗口类型', type=str, choices=["normal", "max", "min", "hide"], default="normal")

# 解析传入的命令行列表而不是sys.argv
try:
    args = parser.parse_args(args_list[1:])  # [1:]是因为args_list的第一个元素是命令名，通常不需要
except BaseException as e:
    pass

user, cmd, window = vars(args)

print(user, cmd, window)
# 使用参数
# print(f"详细程度：{args.verbosity}")
# print(f"回显内容：{args.echo}")
