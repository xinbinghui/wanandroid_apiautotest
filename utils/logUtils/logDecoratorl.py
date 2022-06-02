from functools import wraps
from utils.logUtils.logControl import INFO, WARNING

def log_decorator(switch: bool):
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """
    # 判断参数类型是否是 int 类型
    if isinstance(switch, bool):
        def decorator(func):
            @wraps(func)
            def swapper(*args, **kwargs):
                # 判断日志为开启状态，才打印日志
                res = func(*args, **kwargs)
                # 判断日志开关为开启状态
                if switch:
                    if res is not None:
                        _dependent_case = res['yaml_data']['dependence_case']
                        # 判断如果有依赖数据，则展示
                        if _dependent_case is True:
                            _dependent_case = res['yaml_data']['dependence_case_data']
                        else:
                            _dependent_case = "暂无依赖用例数据"

                        _is_run = res['yaml_data']['is_run']
                        # 判断正常打印的日志，控制台输出绿色
                        if _is_run is None or _is_run is True:
                            INFO.logger.info(
                                f"\n=================================================================================\n"
                                f"测试标题: {res['yaml_data']['detail']}\n"
                                f"请求方式: {res['yaml_data']['method']}\n"
                                f"请求头:   {res['yaml_data']['headers']}\n"
                                f"请求路径: {res['yaml_data']['url']}\n"
                                f"请求内容: {res['yaml_data']['data']}\n"
                                f"依赖测试用例: {_dependent_case}\n"
                                f"接口响应内容: {res['response_data']}\n"
                                f"接口响应时长: {res['res_time']} ms\n"
                                f"数据库断言数据: {res['sql_data']}\n"
                                "================================================================================="
                            )
                        else:
                            # 跳过执行的用例，控制台输出黄色
                            WARNING.logger.warning(
                                f"\n=================================================================================\n"
                                "该条用例跳过执行.\n"
                                f"测试标题: {res['yaml_data']['detail']}\n"
                                f"请求方式: {res['yaml_data']['method']}\n"
                                f"请求头:   {res['yaml_data']['headers']}\n"
                                f"请求路径: {res['yaml_data']['url']}\n"
                                f"请求内容: {res['yaml_data']['data']}\n"
                                f"依赖测试用例: {_dependent_case}\n"
                                f"接口响应内容: {res['response_data']}\n"
                                f"数据库断言数据: {res['sql_data']}\n"
                                "================================================================================="
                            )
                    return res
                else:
                    return res
            return swapper

        return decorator
    else:
        raise TypeError("日志开关只能为 Ture 或者 False")