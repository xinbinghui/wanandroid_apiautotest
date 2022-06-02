import pytest
import requests
import allure
import os
import time
from utils.cacheUtils.cacheControl import Cache
from utils.readfilesUtils.get_all_files_path import get_all_files
from utils.readfilesUtils.get_yaml_data_analysis import CaseData
from common.setting import ConfigHandler
from utils.otherUtils.allureDate.allure_tools import allure_step, allure_step_no
from enums.yamlData_enum import YamlData
from utils.logUtils.logControl import INFO, ERROR, WARNING

@pytest.fixture(scope="session", autouse=True)
def clear_report():
    try:
        for one in os.listdir(ConfigHandler.report_path + '/tmp'):
            if 'json' in one:
                os.remove(ConfigHandler.report_path + f'/tmp/{one}')
            if 'txt' in one:
                os.remove(ConfigHandler.report_path + f'/tmp/{one}')
    except Exception as e:
        print("allure数据清除失败", e)

    yield

@pytest.fixture(scope='session', autouse=True)
def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """
    case_data = {}
    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(ConfigHandler.data_path, yaml_data_switch=True):
        case_process = CaseData(i).case_process(case_id_switch=True)
        # 转换数据类型
        for case in case_process:
            for key, value in case.items():
                # 判断case_id是否已存在
                case_id_exit = key in case_data.keys()
                # 如果case_id不存在，则将用例写入缓存池中
                if case_id_exit is False:
                    case_data[key] = value
                # 当case_id为True存在时，则抛出异常
                elif case_id_exit is True:
                    raise ValueError(f'case_id: {key} 存在重复项, 请修改case_id\n'
                                     f'文件路径: {i}')
    
    Cache('case_process').set_caches(case_data)

@pytest.fixture(scope='session', autouse=True)
def work_login_init():
    """
    获取登录的cookie
    :return:
    """
    url = "https://www.wanandroid.com/user/login"
    data = {
        'username': 18800000001,
        'password': 123456
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # 请求登录接口
    res = requests.post(url=url, data=data, headers=headers, verify=True)
    response_cookies = res.cookies

    cookies = ''
    for key, value in response_cookies.items():
        _cookie = key + '=' + value + ';'
        # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
        cookies +=_cookie
        # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
        Cache('login_cookie').set_caches(cookies)

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时, 将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

# 定义单个标签
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke"
    )

@pytest.fixture(scope="function", autouse=True)
def case_skip(caseinfo):
    """处理跳过用例"""
    if caseinfo['is_run'] is False:
        allure.dynamic.title(caseinfo[YamlData.DETAIL.value])
        allure_step_no(f"请求URL: {caseinfo[YamlData.IS_RUN.value]}")
        allure_step_no(f"请求方式: {caseinfo[YamlData.METHOD.value]}")
        allure_step("请求头: ", caseinfo[YamlData.HEADER.value])
        allure_step("请求数据: ", caseinfo[YamlData.DATA.value])
        allure_step("依赖数据: ", caseinfo[YamlData.DEPENDENCE_CASE_DATA.value])
        allure_step("预期数据: ", caseinfo[YamlData.ASSERT.value])
        pytest.skip()

def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """
    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime

    INFO.logger.info(f"成功用例数: {_PASSED}")
    ERROR.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = round((_PASSED + _SKIPPED) / _TOTAL * 100, 2)
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")