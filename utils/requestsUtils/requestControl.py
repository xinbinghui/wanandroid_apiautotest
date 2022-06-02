import requests
import random
from common.setting import ConfigHandler
from utils.otherUtils.get_conf_data import sql_switch
from utils.readfilesUtils.regularControl import cache_regular
from utils.mysqlUtils.mysqlControl import MysqlDB
from enums.yamlData_enum import YamlData
# from utils.requestsUtils.dependentCase import DependentCase
from enums.requestType_enum import RequestType
from requests_toolbelt import MultipartEncoder
from utils.otherUtils.allureDate.allure_tools import allure_step, allure_step_no, allure_attach
from utils.logUtils.logDecoratorl import log_decorator
from utils.logUtils.runTimeDecoratorl import execution_duration

class RequestControl:
    """封装请求"""
    @classmethod
    def _check_params(cls, response, yaml_data, headers, cookie, res_time):
        """抽离出通用模块, 判断 http_request 方法中的一些数据校验"""
        # 判断数据库开关，开启状态，则返回对应的数据
        if sql_switch() and yaml_data['sql'] is not None:
            sql_data = MysqlDB().assert_execution(sql=yaml_data['sql'], rep=response)
            return {"response_data": response, "sql_data": sql_data, "yaml_data": yaml_data, "headers": headers, "cookie": cookie, "res_time":res_time}
        else:
            # 数据库关闭走的逻辑
            return {"response_data": response, "sql_data": {"sql": None}, "yaml_data": yaml_data, "headers": headers, "cookie": cookie, "res_time":res_time}

    @classmethod
    def file_data_exit(cls, yaml_data, file_data):
        """
        判断上传文件时, data参数是否存在
        """
        # 兼容又要上传文件，又要上传其他类型参数
        try:
            for key, value in yaml_data[YamlData.DATA.value]['data'].items():
                file_data[key] = value
        except KeyError:
            pass

    @classmethod
    def multipart_data(cls, file_data):
        multipart = MultipartEncoder(fields=file_data, boundary='-----------------------------' + str(random.randint(int(1e28), int(1e29-1))))
        return multipart

    @classmethod
    def check_headers_str_null(cls, headers):
        """
        兼容用户未填写headers或者header值为int
        :return:
        """
        if headers is None:
            return {'headers': None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
            return headers

    @classmethod
    def multipart_in_headers(cls, request_data, header):
        """
        判断处理header为 Content-Type: multipart/form-data
        """
        if header is None:
            return request_data, {'headers': None}
        else:
            # 将header中的int转换成str
            for key, value in header.items():
                if not isinstance(value, str):
                    header[key] = str(value)
            if "multipart/form-data" in str(header.values()):
                # 判断请求参数不为空, 并且参数是字典类型
                if request_data and isinstance(request_data, dict):
                    # 当 Content-Type 为 "multipart/form-data"时，需要将数据类型转换成 str
                    for key, value in request_data.items():
                        if not isinstance(value, str):
                            request_data[key] = str(value)
                    
                    request_data = MultipartEncoder(request_data)
                    header['Content-Type'] = request_data.content_type
        
        return request_data, header
    
    @classmethod
    def file_prams_exit(cls, yaml_data, multipart):
        try:
            params = yaml_data[YamlData.DATA.value]['params']
        except:
            params = None
        return params, multipart


    @classmethod
    def text_encode(cls, text):
        """
        unicode 解码
        """
        return text.encode('utf-8').decode('utf-8')

    @classmethod
    def response_elapsed_total_seconds(cls, res):
        """
        获取接口响应时长
        """
        try:
            return res.elapsed.total_seconds()
        except AttributeError:
            return 0.00
    
    @classmethod
    def upload_file(cls, yaml_data):
        """
        判断处理上传文件
        :param yaml_data
        :return:
        """
        # 处理上传多个文件的情况
        _files = []
        file_data = {}
        for key, value in yaml_data[YamlData.DATA.value]['file'].items():
            file_path = ConfigHandler.file_path + value
            file_data[key] = (value, open(file_path, mode='rb'), 'application/octet-stream')
            _files.append(file_data)
            # allure中展示该附件
            allure_attach(source=file_path, name=value, extension=value)
        # 兼容又要上传文件，又要上传其他类型参数
        cls.file_data_exit(yaml_data, file_data)
        multipart = cls.multipart_data(file_data)
        yaml_data[YamlData.HEADER.value]['Content-Type'] = multipart.content_type
        yaml_data, multipart = cls.file_prams_exit(yaml_data,  multipart)
        return yaml_data, multipart

    @log_decorator(True)
    @execution_duration(3000)
    def http_request(self, yaml_data, **kwargs):
        """
        封装请求
        :param yaml_data: 从yaml文件中读取出来的所有数据
        :param kwargs: 接收更多参数
        :return:
        """
        re_data = cache_regular(str(yaml_data))
        yaml_data = eval(re_data)
        _is_run = yaml_data[YamlData.IS_RUN.value]
        _method = yaml_data[YamlData.METHOD.value]
        _detail = yaml_data[YamlData.DETAIL.value]
        _headers = yaml_data[YamlData.HEADER.value]
        _request_type = yaml_data[YamlData.REQUEST_TYPE.value]
        _data = yaml_data[YamlData.DATA.value]
        _sql = yaml_data[YamlData.SQL.value]
        _assert = yaml_data[YamlData.ASSERT.value]
        _dependent_data = yaml_data[YamlData.DEPENDENCE_CASE_DATA.value]

        requests.packages.urllib3.disable_warnings()

        # 判断用例是否执行
        if _is_run is True or _is_run is None:
            # 处理多业务逻辑
            # DependentCase().get_dependent_data(yaml_data=yaml_data)

            if _request_type == RequestType.JSON.value:
                _headers = self.check_headers_str_null(headers=_headers)
                res = requests.request(method=_method, url=yaml_data[YamlData.URL.value], json=_data, headers=_headers, verify=False, **kwargs)


            elif _request_type == RequestType.PARAMS.value:
                if _data is not None:
                    # url拼接的方式传参
                    parama_data = "?"
                    for key, value in _data.items():
                        parama_data += (key + '=' + str(value) + '&')
                    url = yaml_data[YamlData.URL.value] + parama_data[:-1]
                _headers = self.check_headers_str_null(_headers)
                res = requests.request(method=_method, url=url, headers= _headers, verify=False, **kwargs)


            # 判断上传文件
            elif _request_type == RequestType.FILE.value:
                multipart = self.upload_file(yaml_data)
                _headers = self.check_headers_str_null(_headers)
                res = requests.request(method=_method, url=yaml_data[YamlData.URL.value], data=multipart[0], params=multipart[1], headers=_headers, verify= False, **kwargs)


            elif _request_type == RequestType.DATE.value:
                _data, _headers = self.multipart_in_headers(request_data=_data, header=_headers)
                res = requests.request(method=_method, url=yaml_data[YamlData.URL.value], data=_data, headers=_headers, verify=False, **kwargs)


            allure_step_no(f"请求URL: {yaml_data[YamlData.URL.value]}")
            allure_step_no(f"请求方式: {_method}")
            allure_step("请求头: ", _headers)
            allure_step("请求数据: ", _data)
            allure_step("依赖数据: ", _dependent_data)
            allure_step("预期数据: ", _assert)
            _res_time = self.response_elapsed_total_seconds(res)
            allure_step_no(f"响应耗时(s): {_res_time}")

            try:
                res = res.json()
            except:
                res = self.text_encode(res.text)
            try:
                cookie = res.cookies.get_dict()
            except:
                cookie = None

            return self._check_params(response=res, yaml_data=yaml_data, headers=_headers, cookie=cookie, res_time=_res_time)
        else:
            # 用例跳过执行的话，响应数据和sql数据为空
            return {'response_data': False, 'sql_data': False, 'yaml_data': yaml_data, 'res_time': 0.00}