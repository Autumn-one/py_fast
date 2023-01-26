def startswith(l,k):
    """
    传入列表和关键字，返回一个新的列表包含原始列表中以关键字开头的项
    """
    return [i for i in l if i.startswith(k)]

def not_startswith(l,k):
    """
    传入列表和关键字，返回一个新的列表包含原始列表中不以关键字开头的项
    """
    return [i for i in l if not i.startswith(k)]