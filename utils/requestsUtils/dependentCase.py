from utils.cacheUtils.cacheControl import Cache
from enums.yamlData_enum import YamlData
from utils.readfilesUtils.regularControl import regular
from utils.requestsUtils.requestControl import RequestControl
from enums.dependentType_enum import DenpendentType
from utils.otherUtils.jsonpath import jsonpath
from utils.mysqlUtils.mysqlControl import MysqlDB

class DependentCase:

    @classmethod
    def get_cache(cls, case_id):
        """
        获取缓存用例池中的数据, 通过 case_id 提取
        :parama case_id:
        :return: case_id_01
        """
        _case_data = eval(Cache('case_process').get_cache())[case_id]
        return _case_data

    @classmethod
    def jsonpath_data(cls, obj, expr):
        """
        通过jsonpath提取依赖的数据
        :param obj: 对象信息
        :param expr: jsonpath 方法
        :return: 提取到的内容值, 返回是个数组
        对象: {"data": applyID} --> jsonpath提取方法: $.data.data.[0].applyID
        """
        _jsonpath_data = jsonpath(obj, expr)
        # 判断是否正常提取到数据，如未提取到，则抛异常
        if _jsonpath_data is not False:
            return _jsonpath_data
        else:
            raise ValueError(f'jsonpath提取失败! \n 提取的数据: {obj} \n jsonpath规则: {expr}')

    @classmethod
    def url_replace(cls, replace_key, jsonpath_datas, jsonpath_data, case_data):
        """
        url中的动态参数替换
        :param replace_key: 用例中需要替换数据的 replace_key
        :param jsonpath_dates: jsonpath 存放的数据值
        :param jsonpath_data: jsonpath 解析出来的数据值
        :param case_data: 用例数据
        :return:
        """
        # 如: 一般有些接口的参数在url中,并且没有参数名称, /api/v1/work/spu/approval/spuApplyDetails/{id}
        # 那么可以使用如下方式编写用例, 可以使用 $url_params{}替换,
        # 如/api/v1/work/spu/approval/spuApplyDetails/$url_params{id}

        if '$url_param' in replace_key:
            _url = case_data['url'].replace(replace_key, str(jsonpath_data[0]))
            jsonpath_datas['$.url'] = _url
        else:
            jsonpath_datas[replace_key] = jsonpath_data[0]

    @classmethod
    def is_dependent(cls, case_data):
        """
        判断是否有数据依赖
        :return:
        """
        # 获取用例中的dependent_case值, 判断该用例是否需要执行依赖
        _dependent_case = case_data[YamlData.DEPENDENCE_CASE.value]
        # 获取依赖用例数据
        _dependence_case_datas = case_data[YamlData.DEPENDENCE_CASE_DATA.value]
        _setup_sql = case_data[YamlData.SETUP_SQL.value]
        # 判断是否有依赖
        if _dependent_case is True:
            # 读取依赖相关的用例数据
            jsonpath_datas = {}
            # 循环所有需要依赖的数据
            try:
                for dependence_case_data in _dependence_case_datas:
                    dependent_data = dependence_case_data['dependent_data']
                    _case_id = dependence_case_data[YamlData.CASE_ID.value]
                    re_data = regular(str(cls.get_cache(_case_id)))
                    res = RequestControl().http_request(eval(re_data))
                    for i in dependent_data:
                        # _case_id = dependence_case_data[YamlData.CASE_ID.value]
                        _dependent_type = i[YamlData.DEPENDENT_TYPE.value]
                        _jsonpath = i[YamlData.JSONPATH.value]
                        _replace_key = i[YamlData.REPLACE_KEY.value]

                        # 判断依赖数据类型, 依赖response中的数据
                        if _dependent_type == DenpendentType.RESPONSE.value:
                            jsonpath_data = cls.jsonpath_data(res['response_data'], _jsonpath)
                            cls.url_replace(replace_key=_replace_key, jsonpath_datas=jsonpath_datas, jsonpath_data=jsonpath_data, case_data=case_data)
                        # 判断依赖数据类型, 依赖sql中的数据
                        elif _dependent_type == DenpendentType.SQL_DATA.value:
                            if _setup_sql is not None:
                                sql_data = MysqlDB().setup_sql_data(sql=_setup_sql)
                                jsonpath_data = cls.jsonpath_data(obj=sql_data, expr=_jsonpath)
                                jsonpath_datas[_replace_key] = jsonpath_data[0]
                                cls.url_replace(replace_key=_replace_key, jsonpath_datas=jsonpath_datas, jsonpath_data=jsonpath_data, case_data=case_data)
                            else:
                                raise ValueError("当前用例需要获取sql数据, setup_sql中需要填写对应的sql语句。\n"
                                                 "case_id: {0}".format(_case_id))
                        else:
                            raise ValueError("依赖的dependent_type不正确, 只支持request、response、sql依赖\n"
                                             f"当前填写内容: {i[YamlData.DEPENDENT_TYPE.value]}")
                return jsonpath_datas
            except KeyError as e:
                raise KeyError(f"dependence_case_data依赖用例中, 未找到 {e} 参数，请检查是否填写"
                               f"如已填写, 请检查是否存在yaml缩进问题")
            except TypeError:
                raise TypeError("dependence_case_data下的所有内容均不能为空! 请检查相关数据是否填写, 如已填写, 请检查缩进问题")

        else:
            return False

    @classmethod
    def get_dependent_data(cls, yaml_data):
        """
        jsonpath 和 依赖的数据, 进行交换
        :param yaml_data:
        :return:
        """
        # _dependent_data = DependentCase().is_dependent(yaml_data)
        _dependent_data = cls.is_dependent(yaml_data)
        # 判断有依赖
        if _dependent_data is not False:
            for key, value in _dependent_data.items():
                # 通过jsonpath判断出需要替换数据的位置
                _change_data = key.split('.')
                # jsonpath 数据解析
                _new_data = 'yaml_data' + ''
                for i in _change_data:
                    if i == '$':
                        pass
                    elif i[0] == '[' and i[-1] == ']':
                        _new_data += "[" + i[1:-1] + "]"
                    else:
                        _new_data += "[" + "'" + i + "'" + "]"
                # 最终提取到的数据,转换成 yaml_data[xxx][xxx]
                _new_data += ' = value'
                exec(_new_data)