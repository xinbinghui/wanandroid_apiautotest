import pytest
import os
import traceback
from utils.logUtils.logControl import INFO
from utils.otherUtils.get_conf_data import project_name
from utils.readfilesUtils.caseAutomaticControl import TestCaseAutomaticGeneration
from utils.otherUtils.get_conf_data import get_notification_type
from enums.notificationType_enum import NotificationType
from utils.noticUtils.sendmailControl import SendEmail

def run():
    # 从配置文件中获取项目名称
    try:
        INFO.logger.info(
            """
                         _    _         _      _____         _
              __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
             / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
            | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
             \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                  |_|
                  开始执行{}项目...
                """.format(project_name)
        )
        # 判断现有的测试用例，如果未生成测试代码，则自动生成
        TestCaseAutomaticGeneration().get_case_automatic()

        pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                     '--alluredir', './report/tmp', "--clean-alluredir"])
        os.system(r"allure generate ./report/tmp -o ./report/html --clean")

        # 判断通知类型，根据配置发送不同的报告通知
        if get_notification_type() == NotificationType.DEFAULT.value:
            pass
        elif get_notification_type() == NotificationType.EMAIL.value:
            # SendEmail().send_main()
            pass
        else:
            raise ValueError("通知类型配置错误，暂不支持该类型通知")

        # os.system(f"allure serve ./report/tmp -p 9999")
    
    except Exception:
        # 如有异常，相关异常发送邮件
        # e = traceback.format_exc()
        # SendEmail().error_mail(e)
        raise

if __name__ == '__main__':
    run()