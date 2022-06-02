import os
from common.setting import ConfigHandler
from utils.readfilesUtils.testcase_template import write_testcase_file
from utils.readfilesUtils.yamlControl import GetYamlData
from utils.otherUtils.get_os_sep import get_os_sep
from utils.readfilesUtils.get_all_files_path import get_all_files


class TestCaseAutomaticGeneration:
    """自动生成自动化测试中的test_case代码"""

    # TODO 自动生成测试代码
    def __init__(self):
        pass

    @classmethod
    def case_date_path(cls) -> str:
        """返回 yaml 用例文件路径"""
        return ConfigHandler.data_path

    @classmethod
    def case_path(cls) -> str:
        """ 存放用例代码路径"""
        return ConfigHandler.case_path

    def file_name(self, file: str) -> str:
        """
        通过 yaml文件的命名，将名称转换成 py文件的名称
        :param file: yaml 文件路径
        :return:  示例： DateDemo.py
        """
        i = len(self.case_date_path())
        yaml_path = file[i:]
        file_name = None
        # 路径转换
        if '.yaml' in yaml_path:
            file_name = yaml_path.replace('.yaml', '.py')
        elif '.yml' in yaml_path:
            file_name = yaml_path.replace('.yml', '.py')
        return file_name

    def get_package_path(self, file_path: str) -> str:
        """
        根据不同的层级，获取 test_case 中需要依赖的包
        :return: from lib.test_demo import DateDemo
        """
        lib_path = self.file_name(file_path)
        i = lib_path.split(get_os_sep())
        # 判断多层目录下的导报结构
        if len(i) > 1:
            package_path = "from lib"
            for files in i:
                # 去掉路径中的 .py
                if '.py' in files:
                    files = files[:-3]
                package_path += "." + files
            # 正常完整版本的多层结构导包路径
            package_path += ' import' + ' ' + i[-1][:-3]
            return package_path
        # 判断一层目录下的导报结构
        elif len(i) == 1:
            return f"from lib.{i[0][:-3]} import {i[0][:-3]}"

    def get_case_path(self, file_path: str) -> tuple:
        """
        根据 yaml 中的用例，生成对应 testCase 层代码的路径
        :param file_path: yaml用例路径
        :return: D:\\Project\\test_case\\test_case_demo.py, test_case_demo.py
        """
        # 这里通过“\\” 符号进行分割，提取出来文件名称
        path = self.file_name(file_path).split('\\')
        # 判断生成的 testcase 文件名称，需要以test_ 开头
        case_name = path[-1] = path[-1].replace(path[-1], "test_" + path[-1])
        new_name = '\\'.join(path)
        return ConfigHandler.case_path + new_name, case_name

    @classmethod
    def get_testcase_detail(cls, file_path: str) -> str:
        """
        获取用例描述
        :param file_path: yaml 用例路径
        :return:
        """
        return GetYamlData(file_path).get_yaml_data()[0]['detail']

    def get_test_class_title(self, file_path: str) -> str:
        """
        自动生成类名称
        :param file_path:
        :return: sup_apply_list --> SupApplyList
        """
        # 提取文件名称
        _FILE_NAME = os.path.split(self.file_name(file_path))[1][:-3]
        _NAME = _FILE_NAME.split("_")
        # 将文件名称格式，转换成类名称: sup_apply_list --> SupApplyList
        for i in range(len(_NAME)):
            _NAME[i] = _NAME[i].capitalize()
        _CLASS_NAME = "".join(_NAME)

        return _CLASS_NAME

    @classmethod
    def error_message(cls, param_name, file_path):
        """
        用例中填写不正确的相关提示
        :return:
        """
        msg = f"用例中未找到 {param_name} 参数值，请检查新增的用例中是否填写对应的参数内容" \
              "如已填写，可能是 yaml 参数缩进不正确\n" \
              f"用例路径: {file_path}"
        return msg

    def func_title(self, file_path: str) -> str:
        """
        函数名称
        :param file_path: yaml 用例路径
        :return:
        """

        _FILE_NAME = os.path.split(self.file_name(file_path))[1][:-3]
        return _FILE_NAME

    @classmethod
    def allure_epic(cls, case_data: dict, file_path) -> str:
        """
        用于 allure 报告装饰器中的内容 @allure.epic("项目名称")
        :param file_path: 用例路径
        :param case_data: 用例数据
        :return:
        """
        try:
            return case_data['case_common']['allureEpic']
        except KeyError:
            raise KeyError(cls.error_message(
                param_name="allureEpic",
                file_path=file_path
            ))

    @classmethod
    def allure_feature(cls, case_data: dict, file_path) -> str:
        """
        用于 allure 报告装饰器中的内容 @allure.feature("模块名称")
        :param file_path:
        :param case_data:
        :return:
        """
        try:
            return case_data['case_common']['allureFeature']
        except KeyError:
            raise KeyError(cls.error_message(
                param_name="allureFeature",
                file_path=file_path
            ))

    @classmethod
    def allure_story(cls, case_data: dict, file_path) -> str:
        """
        用于 allure 报告装饰器中的内容  @allure.story("测试功能")
        :param file_path:
        :param case_data:
        :return:
        """
        try:
            return case_data['case_common']['allureStory']
        except KeyError:
            raise KeyError(cls.error_message(
                param_name="allureStory",
                file_path=file_path
            ))

    def mk_dir(self, file_path: str) -> None:
        """ 判断生成自动化代码的文件夹路径是否存在，如果不存在，则自动创建 """
        # _LibDirPath = os.path.split(self.libPagePath(filePath))[0]
        _CaseDirPath = os.path.split(self.get_case_path(file_path)[0])[0]
        if not os.path.exists(_CaseDirPath):
            os.makedirs(_CaseDirPath)

    def yaml_path(self, file_path: str) -> str:
        """
        生成动态 yaml 路径, 主要处理业务分层场景
        :param file_path: 如业务有多个层级, 则获取到每一层/test_demo/DateDemo.py
        :return: Login/common.yaml
        """
        i = len(self.case_date_path())
        # 兼容 linux 和 window 操作路径
        yaml_path = file_path[i:].replace("\\", "/")
        return yaml_path

    def get_case_automatic(self) -> None:
        """ 自动生成 测试代码"""
        file_path = get_all_files(ConfigHandler.data_path, yaml_data_switch=True)

        for file in file_path:
            # 判断代理拦截的yaml文件，不生成test_case代码
            if 'proxy_data.yaml' not in file:
                # 判断用例需要用的文件夹路径是否存在，不存在则创建
                self.mk_dir(file)
                yaml_case_process = GetYamlData(file).get_yaml_data()
                write_testcase_file(
                    allure_epic=self.allure_epic(case_data=yaml_case_process, file_path=file),
                    allure_feature=self.allure_feature(yaml_case_process, file_path=file),
                    class_title=self.get_test_class_title(file), func_title=self.func_title(file),
                    case_path=self.get_case_path(file)[0], yaml_path=self.yaml_path(file),
                    file_name=self.get_case_path(file)[1],
                    allure_story=self.allure_story(case_data=yaml_case_process, file_path=file)
                    )

if __name__ == '__main__':
    TestCaseAutomaticGeneration().get_case_automatic()