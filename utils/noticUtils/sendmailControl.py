import os
import smtplib
import zipfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from common.setting import ConfigHandler
from email.mime.multipart import MIMEMultipart
from utils.readfilesUtils.yamlControl import GetYamlData
from utils.readfilesUtils.get_all_files_path import get_all_files
from utils.otherUtils.allureDate.allure_report_data import CaseCount, AllureFileClean


def zipDir():
    zippath = os.path.join(ConfigHandler.report_zip_path, 'API测试报告.zip')
    zip = zipfile.ZipFile(zippath, mode='w')
    filenames = get_all_files(ConfigHandler.report_html_path)
    for filename in filenames:
        # 去掉目标跟路径，只对目标文件夹下面的文件及文件夹进行压缩
        refilename = filename.replace(ConfigHandler.report_html_path, '')
        zip.write(filename, refilename)
    zip.close()
    return zippath

class SendEmail:
    def __init__(self):
        self.getData = GetYamlData(ConfigHandler.config_path).get_yaml_data()['email']
        self.send_user = self.getData['send_user']
        self.email_host = self.getData['email_host']
        self.key = self.getData['stamp_key']
        self.name = GetYamlData(ConfigHandler.config_path).get_yaml_data()['ProjectName'][0]
        self.allureData = CaseCount()
        self.PASS = self.allureData.pass_count()
        self.FAILED = self.allureData.failed_count()
        self.BROKEN = self.allureData.broken_count()
        self.SKIP = self.allureData.skipped_count()
        self.TOTAL = self.allureData.total_count()
        self.RATE = self.allureData.pass_rate()
        self.CaseDetail = AllureFileClean().get_failed_cases_detail()
        """
        self.CaseDetail样式:
        失败用例:
        **********************************
        test_collect_add_tool[新增收藏网址接口]:test_case.collect.test_collect_add_tool.TestCollectAddTool#test_collect_add_tool
        """

    def send_mail(self, user_list, sub, content, file_msg=None):
        """
        :param user_list: 发件人邮箱
        :param sub:
        :param content: 发送内容
        :return:
        """
        user = self.send_user
        # user = "辛炳辉" + "<" + self.send_user + ">"\
        if file_msg is None:
            message = MIMEText(content, _subtype='plain', _charset='utf-8')
        else:
            message = MIMEMultipart()
            message.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))
            message.attach(file_msg)

        message['Subject'] = sub
        message['From'] = user
        message['To'] = ';'.join(user_list)
        server = smtplib.SMTP()
        server.connect(self.email_host, 25)
        server.login(self.send_user, self.key)
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def error_mail(self, error_message):
        """
        执行异常邮件通知
        :param error_message: 报错信息
        :return:
        """
        email = self.getData['send_list']
        user_list = email.split(',')

        sub = self.name + "接口自动化执行异常通知"
        content = "自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下: \n{0}".format(error_message)
        self.send_mail(user_list, sub, content)

    def send_main(self):
        """
        发送邮件
        :return:
        """
        email = self.getData['send_list']
        user_list = email.split(',')

        sub = self.name + "接口自动化报告"
        content = """
        各位同事，大家好：
            自动化用例执行完成，执行结果如下：
            用例运行总数：{} 个
            通过用例个数：{} 个
            失败用例个数：{} 个
            异常用例个数：{} 个
            跳过用例个数：{} 个
            成   功   率：{} %
        
        {}

        **********************************
        jenkins地址：https://121.xx.xx.47:8989/login
        详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息。谢谢。
        """.format(self.TOTAL, self.PASS, self.FAILED, self.BROKEN, self.SKIP, self.RATE, self.CaseDetail)

        with open(zipDir(), mode='rb') as f:
            file_msg = MIMEBase('application', 'octet-stream')
            file_msg.set_payload(f.read())
        encoders.encode_base64(file_msg)
        file_msg.add_header('Content-Disposition', 'attachment', filename='测试报告.zip')
        self.send_mail(user_list, sub, content, file_msg)

if __name__ == '__main__':
    SendEmail().send_main()