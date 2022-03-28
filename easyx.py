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


def is_in(a, b, join="or"):
    """
    传入a和b参数判断 a 是否在 b 中
    """
    if isinstance(a, tuple) or isinstance(a, list): # 后续可以判断迭代器类型, 暂时判断这两个
        if join == 'or':
            return any([i in b for i in a])
        else:
            return all([i in b for i in a])
    else:
        return a in b


def no_in(*args, **kwargs):
    """
    传入a和b参数判断 a 是否不在 b 中
    """
    return not is_in(*args, **kwargs)
