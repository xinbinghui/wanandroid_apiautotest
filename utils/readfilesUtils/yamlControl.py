import os
import yaml.scanner
import yaml

class GetYamlData:

    def __init__(self,file_dir):
        self.filedir = file_dir

    def get_yaml_data(self):
        """
        获取yaml中的数据
        :param: fileDir:
        :return: 
        """
        # 判断文件是否存在
        if os.path.exists(self.filedir):
            with open(self.filedir, mode='r', encoding='utf-8') as f:
                try:
                    res = yaml.load(f, Loader= yaml.FullLoader)
                    return res
                except UnicodeDecodeError:
                    raise ValueError(f'yaml文件编码错误, 文件路径: {self.filedir}')
        
        else:
            raise FileNotFoundError('文件路径不存在')