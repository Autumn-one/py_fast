def is_none(arg):
    """
    传入一个参数判断是否为None
    """
    return arg is None

def no_none(arg):
    """
    传入一个参数判断是否不为None
    """
    return not is_none(arg)

def is_in(a,b):
    """
    传入a和b参数判断 a 是否在 b 中
    """
    return a in b

def no_in(a,b):
    """
    传入a和b参数判断 a 是否不在 b 中
    """
    return not is_in(a,b)