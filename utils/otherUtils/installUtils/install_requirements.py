import os
from common.setting import ConfigHandler
from utils.otherUtils.get_os_sep import get_os_sep
from utils.otherUtils.get_conf_data import get_mirror_url
from utils.logUtils.logControl import INFO
os.system("pip3 install chardet")
import chardet


class InstallRequirements:
    """ 自动识别安装最新的依赖库 """

    def __init__(self):
        self.version_library_comparisons_path = ConfigHandler.util_install_path + "version_library_comparisons.txt"
        self.requirements_path = ConfigHandler.root_path + get_os_sep() + "requirements.txt"
        self.mirror_url = get_mirror_url()
        # 初始化时，获取最新的版本库

        # os.system("pip freeze > {0}".format(self.requirements_path))

    def read_version_library_comparisons_txt(self):
        """
        获取版本比对默认的文件
        @return:
        """
        with open(self.version_library_comparisons_path, 'r', encoding="utf-8") as f:
            return f.read().strip(' ')

    @classmethod
    def check_charset(cls, file_path):
        """获取文件的字符集"""
        with open(file_path, "rb") as f:
            data = f.read(4)
            charset = chardet.detect(data)['encoding']
        return charset

    def read_requirements(self):
        """获取安装文件"""
        file_data = ""
        with open(self.requirements_path, 'r', encoding=self.check_charset(self.requirements_path)) as f:
            for line in f:
                if "[0m" in line:
                    line = line.replace("[0m", "")
                file_data += line

        with open(self.requirements_path, "w", encoding=self.check_charset(self.requirements_path)) as f:
            f.write(file_data)

        return file_data

    def text_comparison(self):
        """
        版本库比对
        @return:
        """
        read_version_library_comparisons_txt = self.read_version_library_comparisons_txt()
        read_requirements = self.read_requirements()
        if read_version_library_comparisons_txt == read_requirements:
            INFO.logger.info("程序中未检查到更新版本库，已为您跳过自动安装库")
        # 程序中如出现不同的文件，则安装
        else:
            INFO.logger.info("程序中检测到您更新了依赖库，已为您自动安装")
            os.system("pip3 install -r {0}".format(self.requirements_path))
            with open(self.version_library_comparisons_path, "w",
                      encoding=self.check_charset(self.requirements_path)) as f:
                f.write(read_requirements)


if __name__ == '__main__':
    InstallRequirements().text_comparison()