from enum import Enum, unique

@unique
class DenpendentType(Enum):
    """
    数据依赖相关枚举
    """
    # 依赖响应中数据
    RESPONSE= 'response'
    # 依赖请求中数据
    REQUEST = 'request'
    # 依赖sql中数据
    SQL_DATA = 'sqlData'
    # 依赖存入缓存中数据
    CACHE = 'cache'