#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022-06-01 17:42:33
# @Author : 菜头


import allure
import pytest
from common.setting import ConfigHandler
from utils.readfilesUtils.get_yaml_data_analysis import CaseData
from utils.assertUtils.assertControl import Assert
from utils.requestsUtils.requestControl import RequestControl
from utils.readfilesUtils.regularControl import regular
from utils.requestsUtils.dependentCase import DependentCase


TestData = CaseData(ConfigHandler.data_path + r'Collect/collect_delete_tool.yaml').case_process()
re_data = regular(str(TestData))


@allure.epic("开发平台接口")
@allure.feature("收藏模块")
class TestCollectDeleteTool:

    @allure.story("删除收藏网站接口")
    @pytest.mark.parametrize('caseinfo', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_collect_delete_tool(self, caseinfo, case_skip):
        """
        :param :
        :return:
        """
        DependentCase().get_dependent_data(caseinfo)
        res = RequestControl().http_request(caseinfo)
        Assert(caseinfo['assert']).assert_equality(response_data=res['response_data'], 
                                                  sql_data=res['sql_data'])


if __name__ == '__main__':
    pytest.main(['test_collect_delete_tool.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
