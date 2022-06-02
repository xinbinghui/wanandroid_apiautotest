import os

def get_os_sep():
    """
    判断不同的操作系统的路径
    :return: windows 返回"\", linux 返回"/"
    """
    return os.sep