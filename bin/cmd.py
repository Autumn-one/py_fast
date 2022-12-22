import sys
import importlib
from colorama import init, Style, Fore, Back

init()
osx = importlib.import_module("osx")

args = sys.argv

fn_str = args[1].replace("-","_")
fn_args = args[2:]


if fn_str in dir(osx):
    ret = getattr(osx,fn_str)(*fn_args)
    print(ret)
else:
    print(f"{Fore.RED}{Style.BRIGHT}错误的指令!")