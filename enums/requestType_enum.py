from enum import Enum

class RequestType(Enum):
    """
    request 请求发送, 请求参数的数据类型
    """
    # json 类型
    JSON = 'JSON'
    # param 类型
    PARAMS = 'PARAMS'
    # data 类型
    DATE = 'DATE'
    # 文件类型
    FILE = 'FILE'