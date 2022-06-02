import json
from common.setting import ConfigHandler
from utils.readfilesUtils.get_all_files_path import get_all_files

class AllureFileClean:
    """allure 报告数据清洗, 提取业务需要的数据"""

    @classmethod
    def get_testcases(cls):
        """获取所有allure报告中执行用例的情况"""
        # 将所有数据都收集到files中
        files = []
        for i in get_all_files(ConfigHandler.report_path + '/html/data/test-cases'):
            with open(i, mode='r', encoding='utf-8') as fp:
                data = json.load(fp)
                files.append(data)
        return files

    def get_failed_case(self) -> list:
        """ 获取到所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcases():
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        return error_case

    def get_failed_cases_detail(self) -> str:
        """ 返回所有失败的测试用例相关内容 """
        date = self.get_failed_case()
        # 判断有失败用例，则返回内容
        if len(date) >= 1:
            values = "失败用例:\n"
            values += "        **********************************\n"
            for i in date:
                values += "        " + i[0] + ":" + i[1] + "\n"
            return values
        else:
            # 如果没有失败用例，则返回False
            return ""

    @classmethod
    def get_case_count(cls) -> dict:
        """ 统计用例数量 """
        fil_name = ConfigHandler.report_path + '/html/widgets/summary.json'
        with open(fil_name, 'r', encoding='utf-8') as fp:
            date = json.load(fp)
        return date


class CaseCount:
    def __init__(self):
        self.AllureData = AllureFileClean()

    def pass_count(self) -> int:
        """用例成功数"""
        return self.AllureData.get_case_count()['statistic']['passed']

    def failed_count(self) -> int:
        """用例失败数"""
        return self.AllureData.get_case_count()['statistic']['failed']

    def broken_count(self) -> int:
        """用例异常数"""
        return self.AllureData.get_case_count()['statistic']['broken']

    def skipped_count(self) -> int:
        """用例跳过数"""
        return self.AllureData.get_case_count()['statistic']['skipped']

    def total_count(self) -> int:
        """用例总数"""
        return self.AllureData.get_case_count()['statistic']['total']

    def pass_rate(self) -> float:
        """用例成功率"""
        # 四舍五入，保留2位小数
        try:
            pass_rate = round((self.pass_count() + self.skipped_count()) / self.total_count() * 100, 2)
            return pass_rate
        except ZeroDivisionError:
            return 0.00

    def get_times(self):
        """用例执行时长"""
        run_time = round(self.AllureData.get_case_count()['time']['duration'] / 1000, 2)
        return run_time